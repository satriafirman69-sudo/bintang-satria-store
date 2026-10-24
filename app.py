
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "bintangsatriashop-demo-key-2026"

PRODUCTS = [
    {"id": 1, "name": "Headphone Wireless", "category": "Elektronik",
     "price": 185000, "emoji": "🎧",
     "description": "Headphone nyaman untuk musik dan belajar."},
    {"id": 2, "name": "Smartwatch Sport", "category": "Elektronik",
     "price": 275000, "emoji": "⌚",
     "description": "Jam tangan modern untuk aktivitas sehari-hari."},
    {"id": 3, "name": "Tas Casual", "category": "Fashion",
     "price": 150000, "emoji": "🎒",
     "description": "Tas praktis untuk kuliah dan bepergian."},
    {"id": 4, "name": "Sepatu Sneakers", "category": "Fashion",
     "price": 320000, "emoji": "👟",
     "description": "Sepatu santai dengan desain kekinian."},
    {"id": 5, "name": "Botol Minum", "category": "Aksesori",
     "price": 45000, "emoji": "🥤",
     "description": "Botol minum untuk menemani aktivitas."},
    {"id": 6, "name": "Lampu Meja", "category": "Aksesori",
     "price": 95000, "emoji": "💡",
     "description": "Lampu meja untuk belajar dan bekerja."}
]


@app.template_filter("rupiah")
def rupiah(value):
    return "Rp{:,.0f}".format(value).replace(",", ".")


@app.context_processor
def cart_counter():
    return {"cart_count": sum(session.get("cart", {}).values())}


def get_cart():
    cart_data = session.get("cart", {})
    items = []

    for product in PRODUCTS:
        quantity = cart_data.get(str(product["id"]), 0)

        if quantity > 0:
            item = product.copy()
            item["quantity"] = quantity
            item["subtotal"] = product["price"] * quantity
            items.append(item)

    return items


@app.route("/")
def home():
    return render_template("home.html", products=PRODUCTS[:3])


@app.route("/produk")
def products():
    keyword = request.args.get("q", "").strip().lower()

    filtered = [
        p for p in PRODUCTS
        if keyword in p["name"].lower()
        or keyword in p["category"].lower()
    ]

    return render_template(
        "products.html", products=filtered, keyword=keyword
    )


@app.route("/tambah/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = next(
        (p for p in PRODUCTS if p["id"] == product_id), None
    )

    if not product:
        flash("Produk tidak ditemukan.", "error")
        return redirect(url_for("products"))

    cart_data = session.get("cart", {})
    key = str(product_id)
    cart_data[key] = cart_data.get(key, 0) + 1
    session["cart"] = cart_data

    flash("Produk berhasil ditambahkan ke keranjang.", "success")
    return redirect(request.referrer or url_for("products"))


@app.route("/keranjang")
def cart():
    items = get_cart()
    total = sum(item["subtotal"] for item in items)

    return render_template("cart.html", items=items, total=total)


@app.route("/hapus/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart_data = session.get("cart", {})
    cart_data.pop(str(product_id), None)
    session["cart"] = cart_data

    flash("Produk berhasil dihapus.", "success")
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items = get_cart()
    total = sum(item["subtotal"] for item in items)

    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        email = request.form.get("email", "").strip()
        alamat = request.form.get("alamat", "").strip()

        if not items:
            flash("Keranjang masih kosong.", "error")
            return redirect(url_for("products"))

        if not nama or not email or not alamat:
            flash("Semua kolom wajib diisi.", "error")
        else:
            session["cart"] = {}
            flash(
                f"Pesanan demo berhasil dibuat atas nama {nama}.",
                "success"
            )
            return redirect(url_for("home"))

    return render_template(
        "checkout.html", items=items, total=total
    )


if __name__ == "__main__":
    app.run(debug=True)
