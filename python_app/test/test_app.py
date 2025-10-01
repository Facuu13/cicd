import python_app.app as app

def test_sumar():
    assert app.sumar(2, 3) == 5

def test_es_par_true():
    assert app.es_par(4) is True

def test_es_par_false():
    assert app.es_par(5) is False
