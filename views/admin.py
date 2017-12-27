from yamath.decorators import *
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from yamath.dbhelper import DoesNotExist
from yamath.dbhelper import User
from yamath.dbhelper import Node
from yamath import app
from yamath.passwordhelper import PH

@app.route("/admin")
@admin_required
def admin():
    return render_template("admin.html")

@app.route("/admin/nodes")
@admin_required
def adminNodes():
    nodes = Node.objects.all()
    return render_template("admin_nodes.html", nodes=nodes)

@app.route("/admin/nodes/add", methods=["POST"])
@admin_required
def adminAddNode():
    node_name = request.form.get("name")
    Node(name=node_name).save()
    return redirect(url_for('adminNodes'))

@app.route("/admin/node/add_ante/<node_id>", methods=["POST"])
@admin_required
def adminNodeAddAnte(node_id):
    node = Node.objects.get(id=node_id)
    ante = Node.objects.get(id=request.form.get("ante_id"))
    node.antes.append(ante)
    node.save()
    Node.update_posts(ante)
    return redirect(url_for("adminNodeDetail", node_id=node_id))

@app.route("/admin/node/rem_ante/<node_id>", methods=["POST"])
@admin_required
def adminNodeRemAnte(node_id):
    node = Node.objects.get(id=node_id)
    ante = Node.objects.get(id=request.form.get("ante_id"))
    node.antes.remove(ante)
    node.save()
    Node.update_posts(ante)
    return redirect(url_for("adminNodeDetail", node_id=node_id))

@app.route("/admin/node_detail/<node_id>")
@admin_required
def adminNodeDetail(node_id):
    node = Node.objects.get(id=node_id)
    nodes = Node.objects.all()
    return render_template("admin_node_detail.html", node=node, nodes=nodes)

@app.route("/admin/node/edit_name/<node_id>", methods=["POST"])
@admin_required
def adminNodeEditName(node_id):
    node = Node.objects.get(id=node_id)
    node.name = request.form.get("name")
    node.save()
    return redirect(url_for("adminNodeDetail", node_id=node_id))

@app.route("/admin/nodes/rem", methods=["POST"])
@admin_required
def adminRemNode():
    node_name = request.form.get("name")
    Node.objects.get(name=node_name).delete()
    return redirect(url_for('adminNodes'))

@app.route("/admin/user_profile/<user_profile_email>")
@admin_required
def adminUserProfile(user_profile_email):
    user_profile = User.objects.get(email=user_profile_email)
    return render_template("admin_user_profile.html", user_profile=user_profile)

@app.route("/admin/user_profile/<user_profile_email>/edit/hashed", methods=["POST"])
@admin_required
def adminUserProfileEditHashed(user_profile_email):
    pw1 = request.form.get("pw1")
    pw2 = request.form.get("pw2")
    user_profile = User.objects.get(email=user_profile_email)
    try:
        assert pw1 == pw2
        user_profile.hashed = PH.get_hash(pw1, user_profile.salt)
        user_profile.save()
    except:
        pass
    return redirect(url_for("adminUserProfile", user_profile_email=user_profile_email))

@app.route("/admin/user_profile/<user_profile_email>/edit/is_active", methods=["POST"])
@admin_required
def adminUserProfileEditIsActive(user_profile_email):
    user_profile = User.objects.get(email=user_profile_email)
    user_profile.is_active = not user_profile.is_active
    user_profile.save()
    return redirect(url_for("adminUserProfile", user_profile_email=user_profile_email))

@app.route("/admin/user_profile/<user_profile_email>/edit/is_admin", methods=["POST"])
@admin_required
def adminUserProfileEditIsAdmin(user_profile_email):
    user_profile = User.objects.get(email=user_profile_email)
    user_profile.is_admin = not user_profile.is_admin
    user_profile.save()
    return redirect(url_for("adminUserProfile", user_profile_email=user_profile_email))

@app.route("/admin/user_profile/<user_profile_email>/edit/is_teacher", methods=["POST"])
@admin_required
def adminUserProfileEditIsTeacher(user_profile_email):
    user_profile = User.objects.get(email=user_profile_email)
    user_profile.is_teacher = not user_profile.is_teacher
    user_profile.save()
    return redirect(url_for("adminUserProfile", user_profile_email=user_profile_email))

@app.route("/admin/users")
@admin_required
def adminUsers():
    users = list(User.objects.filter({}))
    return render_template("admin_users.html", users=users)
