from pc_optimizer.pareto import pareto_front

def test_pareto_removes_dominated_builds():
    rows=[{"cost":900,"ai":80,"animation":80,"gaming":80},{"cost":950,"ai":79,"animation":80,"gaming":80},{"cost":1000,"ai":90,"animation":85,"gaming":88}]
    assert pareto_front(rows) == [rows[0], rows[2]]
