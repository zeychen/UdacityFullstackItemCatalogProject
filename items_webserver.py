from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify


# import database functions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from items_db_setup import Base, Categories, Items
from items_db_query import db_categories, db_items, db_category, db_item

# import user auth functions
from flask import session as login_session
import random, string


# set up server for gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']


# Create session and connect to DB
engine = create_engine('sqlite:///categories.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

"""
User Authentication
"""


@app.route('/login')
def showLogin():
	"""
	anti-forgery state token
	"""
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
	login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
	return render_template('login.html', state=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])

    print "%s" % login_session['access_token']
    print "%s" % login_session['gplus_id']
    print "%s" % login_session['username']
    print "%s" % login_session['email']

    print "done!"
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
	print login_session['username']
	credentials = login_session

	if credentials is None:
		print 'Credentials is None'
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# access_token = credentials.access_token
	print 'In gdisconnect access token is %s', login_session['username']
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	print 'result is '
	print result

	if result['status'] == '200':
		del login_session['access_token'] 
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		response = make_response(json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response


"""
User Authorization
"""


# def createUser(login_session):
#     newUser = User(name=login_session['username'], email=login_session[
#                    'email'], picture=login_session['picture'])
#     db_session.add(newUser)
#     db_session.commit()
#     user = session.query(User).filter_by(email=login_session['email']).one()
#     return user.id


# def getUserInfo(user_id):
#     user = db_session.query(User).filter_by(id=user_id).one()
#     return user


# def getUserID(email):
#     try:
#         user = db_session.query(User).filter_by(email=email).one()
#         return user.id
#     except:
#         return None


def loggedIn(login_session):
	"""
	check if user is logged in
	"""
	return login_session is not None 



"""
JSON APIs
"""


@app.route('/catalog/JSON')
def allCategoriesJSON():
	"""
	list all categories in JSON format
	"""
	categories=db_categories(db_session)
	return jsonify(Categories=[i.serialize for i in categories])


@app.route('/<int:category_id>/items/JSON')
def allItemsJSON(category_id):
	"""
	list all items in JSON format
	"""
	category = db_category(db_session, category_id)
	items = db_items(db_session, category_id)
	return jsonify(Items=[i.serialize for i in items])


"""
Webpages
"""


@app.route('/')
@app.route('/catalog/')
def allCategories():
	"""
	list all categories
	front page
	"""
	categories=db_categories(db_session)
	return render_template('categories.html', categories = categories, user_is_logged_in=loggedIn(login_session))


@app.route('/catalog/newcategory', methods=['GET', 'POST'])
def addCategory():
	"""
	add new category
	requires name of category
	"""

	print login_session['username']

	if 'username' not in login_session:
		return redirect(url_for('showLogin'))
	if request.method == 'POST':
		if request.form['name']:
			newCat = Categories(name=request.form['name'], user_id=login_session['user_id'])
			db_session.add(newCat)
			db_session.commit
			return redirect(url_for('allCategories'))
		else:
			error = "must enter name for category"
			return render_template('newcat.html', error=error)
	else:
		return render_template('newcat.html')


@app.route('/<int:category_id>/deletecategory', methods=['GET', 'POST'])
def deleteCategory(category_id):
	"""
	delete category
	"""
	if 'username' not in login_session:
		return redirect(url_for('showLogin'))
	if request.method == 'POST':
		category = db_category(session, category_id)
		db_session.delete(category)
		db_session.commit()
		return redirect(url_for('allCategories'))
	else:
		category = db_category(db_session, category_id)
		return render_template('deleteCategory.html', name=category.name)


@app.route('/<int:category_id>/items')
def allItems(category_id):
	"""
	list all categories
	front page
	"""
	category = db_category(db_session, category_id)
	items = db_items(db_session, category_id)
	return render_template('items.html', items = items, category = category, user_is_logged_in=loggedIn(login_session))



@app.route('/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
	"""
	edit items within category
	requires name and description
	"""
	if 'username' not in login_session:
		return redirect(url_for('showLogin'))
	if request.method == 'POST':
		if request.form['name'] and request.form['description']:
			item = db_item(db_session, item_id)
			item.name = request.form['name']
			item.description = request.form['description']
			db_session.commit()
			return redirect(url_for('allItems', category_id=category_id))
		else:
			name = request.form['name']
			description = request.form['description']
			category = db_category(db_session, category_id)
			item = db_item(db_session, item_id)
			error = "must enter name and description"
			return render_template('edititem.html', category = category, item = item, name=name, description=description, error=error)
	else:
		category = db_category(db_session, category_id)
		item = db_item(db_session, item_id)
		return render_template('edititem.html', category = category, item = item, name=item.name, description=item.description)


@app.route('/<int:category_id>/item/new', methods=['GET', 'POST'])
def newItem(category_id):
	"""
	add items within category
	requires name and description
	"""
	if 'username' not in login_session:
		return redirect(url_for('showLogin'))
	if request.method == 'POST':
		if request.form['name'] and request.form['description']:
			newItem = Items(name=request.form['name'], description=request.form['description'], category_id = category_id, user_id=login_session['user_id'])
			db_session.add(newItem)
			db_session.commit()
			return redirect(url_for('allItems', category_id=category_id))
		else:
			name = request.form['name']
			description = request.form['description']
			category = db_category(db_session, category_id)
			error = "must enter name and description"
			return render_template('newitem.html', category = category, name=name, description=description, error=error)
	else:
		category = db_category(db_session, category_id)
		return render_template('newitem.html', category = category)


@app.route('/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
	"""
	delete items within category
	"""
	if 'username' not in login_session:
		return redirect(url_for('showLogin'))
	if request.method == 'POST':
		item = db_item(db_session, item_id)
		db_session.delete(item)
		db_session.commit()
		return redirect(url_for('allItems', category_id=category_id, item_id=item_id))
	else:
		item = db_item(db_session, item_id)
		category = db_category(db_session, category_id)
		return render_template('deleteItem.html', category = category, item = item, name=item.name, description=item.description)


if __name__ == '__main__':
	app.secret_key = "xAZ8YHkG5rV6F3Wix4QG7plI"
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
