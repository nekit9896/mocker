from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mock_storage.db"
db = SQLAlchemy(app)


class Mocker(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # заполняется автоматически т к primary_key
    q = db.Column(db.String(128), index=True, unique=True)
    response = db.Column(db.Text)
    description = db.Column(db.String(140))
    last_modified = db.Column(
        db.DateTime, default=datetime.utcnow()
    )  # заполняется автоматически т к default

    def __repr__(
        self,
    ):  # указал что когда мы будем выбирать какой-либо объект на основе класса Mocker,
        # который представляет из себя определенную запись
        return (
            "<Mockers %r>" % self.q
        )  # выдаётся объект и его айди. Возможно name это будет q


@app.route("/index")
def index():
    return render_template("index_voice.html")


@app.route("/create_mock", methods=["GET", "POST"])
def create_mock():
    if request.method == "POST":
        q = request.form["q"]
        response = request.form["response"]
        description = request.form["description"]

        mock = Mocker(
            q=q, response=response, description=description
        )  # передаем в класс полученные значения
        try:
            db.session.add(
                mock
            )  # добавил объект к индексу для последующего комита в базу данных (как с git)
            db.session.commit()  # сохраняем объект в базе данных
            return redirect("/get_mock")
        except:
            return "При сохранении произошла ошибка"

    else:
        return render_template("create_mock.html")


@app.route("/get_mock")
def get_mock():
    get_mocks = Mocker.query.order_by(
        Mocker.last_modified.desc()
    ).all()  # из объекта Mocker получаем записи и сортируем их order_by
    # по дате сохранения. В перспективе можно сортировать по скилам.
    return render_template(
        "get_mock_voice.html", get_mocks=get_mocks
    )  # передаем в шаблон список
    # который называется get_mocks, при этом в самом шаблоне get_mocks мы будем иметь доступ к списку
    # по названию get_mocks


@app.route("/<int:id>")
def get_mocks_by_q(id):
    get_mock_by_id = Mocker.query.get(id)
    return render_template("get_mock_by_id.html", get_mock_by_id=get_mock_by_id)


@app.route("/<int:id>/del")
def mock_delete(id):
    del_mock_by_id = Mocker.query.get_or_404(id)

    try:
        db.session.delete(
            del_mock_by_id
        )  # добавил объект к индексу для последующего комита в базу данных (как с git)
        db.session.commit()  # сохраняем объект в базе данных
        return redirect("/get_mock")
    except:
        return "При удалении произошла ошибка"


@app.route("/<int:id>/update", methods=["GET", "POST"])
def mock_update(id):  # редактирование ранее сохраненного мока
    get_mock_by_id_to_update = Mocker.query.get(
        id
    )  # сначала получаем объект для редактирования записи
    if request.method == "POST":  # такое же добавление записи как и в create_mock
        get_mock_by_id_to_update.q = request.form[
            "q"
        ]  # в поля объекта вставляем новые данные
        get_mock_by_id_to_update.response = request.form["response"]
        get_mock_by_id_to_update.description = request.form["description"]

        try:
            db.session.commit()  # сохраняем объект в базе данных
            return redirect("/get_mock")
        except:
            return "При редактировании произошла ошибка"

    else:
        return render_template(
            "mock_update.html", get_mock_by_id_to_update=get_mock_by_id_to_update
        )


@app.route("/how_to_mock/<string:name>/<string:q>")
def how_to_mock():
    return render_template("how_to_mocker_voice.html")


if (
    __name__ == "__main__"
):  # проверяем что если название файла запуска main то это главная программа
    app.run(debug=True)
