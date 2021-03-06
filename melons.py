from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

# FIXME, we should fix this or delete g for this webapp, set session down in login/
@app.before_request
def before_request():
    if 'email' in session:
        g.status = "Log Out"
    else:
        g.status = "Log In"

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    cartmelon = {}
    total_cost = 0

    #examine our session cookie for a key of cart and pull out the values into a list
    if session.get('cart'):
        cartlist = session['cart']

    #loop through list to add each cart id melon name and price to cart list
        for id in cartlist:
            melon = model.get_melon_by_id(id)
            #if melon id already in our dictionary --> increase qty by one and add melon price to total:            
            if cartmelon.get(melon.id) == None:
                cartmelon[melon.id] = [melon.common_name, 1, melon.price]
            else: 
                cartmelon[melon.id][1] +=1
            total_cost += melon.price
    print "MELON CART"    
    print session
    return render_template("cart.html", cartmelon = cartmelon, total_cost = total_cost)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """
    if session.get('cart') == None:
        session['cart'] = [id]
    else:
        session['cart'].append(id)
    
    flash("Your melon has been added to the cart.")
    return redirect("/cart")

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""

    email = request.form['email']
    password = request.form['password']    

    user = model.get_customer_by_email(email)

    #display name, give log out option, flash success msg, redirect to melons   
    if user != None:
        if user.email == email and user.password == password:
            session['email'] = email
            flash("Hello %s %s! Login successful."% (user.givenname, user.surname))
            return redirect("/melons")
        else:
            flash("Incorrect password! Try again.")
            return redirect("/login")

    else: 
        flash("Sorry only registered customers can log in.")
        return redirect("/login")

@app.route("/logout", methods=["GET"])
def log_out():
    session.clear()
    flash("You are successfully logged out!")
    return redirect("/login")
        
@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
