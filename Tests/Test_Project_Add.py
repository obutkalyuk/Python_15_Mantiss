from model.project import Project

def test_add_project(app):
    project = Project().random()
    new_project = project
    app.go_to_control_page()
    old_projects = app.project.get_project_list()
    app.project.create(new_project)
    new_projects = app.project.get_project_list()
    old_projects.append(new_project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
