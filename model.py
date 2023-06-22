from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session, url_for)

from views import (check_user, create_ticket_to_db, delete_ticket_from_db,
                   edit_user_from_db, get_all_users_from_db,
                   register_user_to_db, update_ticket_to_db,
                   view_ticket_by_id_from_db, view_tickets_from_db,
                   view_user_from_db)

main_route = Blueprint("main", __name__)


@main_route.route("/")
def index():
    return render_template("login.html")


@main_route.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        existing_users = get_all_users_from_db()
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        birth_date = request.form["birth_date"]
        address = request.form["address"]
        email_address = request.form["email_address"]
        password = request.form["password"]

        if username not in existing_users:
            register_user_to_db(
                first_name,
                last_name,
                username,
                birth_date,
                address,
                email_address,
                password,
            )
            return redirect(url_for("main.index"))
        else:
            print("user exists")
            error = "Username already taken."
            return render_template("register.html", error=error)
    else:
        return render_template("register.html", error=None)


@main_route.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # print(check_user(username, password))
        # print(session)
        if check_user(username, password):
            session["username"] = username

        return redirect(url_for("main.home"))
    else:
        return redirect(url_for("main.index"))


@main_route.route("/home", methods=["POST", "GET"])
def home():
    if "username" in session:
        username = session["username"]
        res = view_tickets_from_db(username)
        session["possible_id"] = [item["id"] for item in res]
        return render_template("home.html", res=res, username=session["username"])
    else:
        return "Username or Password is wrong!"


@main_route.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


@main_route.route("/create_ticket", methods=["POST", "GET"])
def create_ticket():
    if request.method == "POST":
        username = session["username"]
        data = request.get_json()

        # Print the attributes of the form data
        ticket_title = data.get("ticketTitle")
        ticket_type = data.get("ticketType")
        ticket_status = data.get("ticketStatus")
        description = data.get("description")

        create_ticket_to_db(
            username, ticket_title, ticket_type, ticket_status, description
        )
        flash("Ticket edited Successfully", "success")
        # Return a JSON response indicating success
        return jsonify({"message": "Ticket created successfully"})
    else:
        return render_template("create_ticket.html")


@main_route.route("/about_us", methods=["POST", "GET"])
def about_us():
    return render_template("about.html")


@main_route.route("/view_tickets/<int:ticket_number>", methods=["GET"])
def delete_ticket(ticket_number):
    print(ticket_number)
    if ticket_number in session["possible_id"]:
        delete_ticket_from_db(ticket_number)
        return jsonify({"message": "Resource deleted successfully"})
    else:
        return jsonify({"message": "Resource not found"}), 404


@main_route.route("/see_ticket/<int:ticket_number>", methods=["GET"])
def view_ticket_by_id(ticket_number):
    if ticket_number in session["possible_id"]:
        # print("received ticket no", ticket_number)
        res = view_ticket_by_id_from_db(ticket_number)
        # print(res)
        return render_template("seeTicket.html", res=res)
    else:
        return jsonify({"message": "Resource not found"}), 404


@main_route.route("/update_ticket/<int:ticket_number>", methods=["POST", "GET"])
def update_ticket(ticket_number):
    if request.method == "POST":
        # print("here")
        if ticket_number in session["possible_id"]:
            print("ticket_number", ticket_number)
            data = request.get_json()
            print("update ticket", data)
            ticket_title = data.get("ticket_title")
            ticket_type = data.get("ticket_type")
            ticket_status = data.get("status_name")
            description = data.get("description")

            update_ticket_to_db(
                ticket_number, ticket_title, ticket_type, ticket_status, description
            )
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Unauthorized access"})
    else:
        return render_template("create_ticket.html")


@main_route.route("/edit_customer_detail", methods=["POST", "GET"])
def edit_customer_detail():
    username = session["username"]
    user_data = view_user_from_db(username)
    return render_template("edit_customer_detail.html", user_data=user_data)


@main_route.route("/update_details", methods=["POST", "GET"])
def update_details():
    if request.method == "POST":
        username = session["username"]
        data = request.get_json()

        print("update user", data)
        firstName = data.get("firstName")
        lastName = data.get("lastName")
        dob = data.get("dob")
        address = data.get("address")
        email = data.get("email")
        password = data.get("password")

        edit_user_from_db(firstName, lastName, username, dob, address, email, password)
        flash("Info edited Successfully", "success")
        return jsonify({"success": True})
