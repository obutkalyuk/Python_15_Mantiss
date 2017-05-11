from model.project import Project


def test_add_project(app):
    project = Project().random()
    new_project = project
    app.go_to_control_page()
    old_projects = app.soap.get_project_list("administrator", "root")
    app.project.create(new_project)
    new_projects = app.soap.get_project_list("administrator", "root")
    old_projects.append(new_project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
