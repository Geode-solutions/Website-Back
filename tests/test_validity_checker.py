import os
import base64

import geode_objects

geode_objects_list = geode_objects.objects_list()

ID = os.environ.get("ID")
base_route = f"/{ID}/validity_checker"


def test_versions(client):
    response = client.get(f"{base_route}/versions")
    assert response.status_code == 200
    versions = response.json["versions"]
    assert type(versions) is list
    for version in versions:
        assert type(version) is dict


def test_allowed_files(client):
    response = client.get(f"{base_route}/allowed_files")
    assert response.status_code == 200
    extensions = response.json["extensions"]
    assert type(extensions) is list


def test_allowed_objects(client):
    # Normal test with filename 'corbi.og_brep'
    for geode_object in geode_objects_list.keys():
        inputs = geode_objects_list[geode_object]["input"]
        for input in inputs:
            for input_extension in input.list_creators():
                response = client.post(
                    f"{base_route}/allowed_objects",
                    data={"filename": f"test.{input_extension}"},
                )
                assert response.status_code == 200
                allowed_objects = response.json["allowed_objects"]
                assert type(allowed_objects) is list
                assert len(allowed_objects) > 0

    # Test with stupid filename
    response = client.post(
        f"{base_route}/allowed_objects", data={"filename": "toto.tutu"}
    )
    assert response.status_code == 200
    allowed_objects = response.json["allowed_objects"]
    assert type(allowed_objects) is list
    assert not allowed_objects

    # Test without filename
    response = client.post(f"{base_route}/allowed_objects")
    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No filename sent"


def test_upload_file(client):
    file = base64.b64encode(open("./tests/data/test.og_brep", "rb").read())
    filename = "test.og_brep"
    filesize = os.path.getsize("./tests/data/test.og_brep")

    # Test with file
    response = client.post(
        f"{base_route}/upload_file",
        data={"file": file, "filename": filename, "filesize": filesize},
    )

    assert response.status_code == 200
    message = response.json["message"]
    assert message == "File uploaded"

    # Test without file
    response = client.post(
        f"{base_route}/upload_file", data={"filename": filename, "filesize": filesize}
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No file sent"

    # Test without filename
    response = client.post(
        f"{base_route}/upload_file", data={"file": file, "filesize": filesize}
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No filename sent"

    # Test without filesize
    response = client.post(
        f"{base_route}/upload_file",
        data={
            "file": file,
            "filename": filename,
        },
    )

    assert response.status_code == 400
    error_description = response.json["description"]
    assert error_description == "No filesize sent"


def test_test_names(client):
    for geode_object in geode_objects_list.keys():
        print(f"{geode_object=}")
        inputs = geode_objects_list[geode_object]["input"]

        for input in inputs:
            for input_extension in input.list_creators():
                print(f"{input_extension=}")
                filename = f"test.{input_extension}"
                file = base64.b64encode(
                    open(f"./tests/data/test.{input_extension}", "rb").read()
                )
                filesize = int(os.path.getsize(f"./tests/data/test.{input_extension}"))

    for geode_object in geode_objects_list.keys():
        # Normal test with all objects
        response = client.post(
            f"{base_route}/tests_names", data={"geode_object": geode_object}
        )
        assert response.status_code == 200
        model_checks = response.json["model_checks"]

        assert type(model_checks) is list
        for model_check in model_checks:
            assert type(model_check) is dict
            is_leaf = model_check["is_leaf"]
            route = model_check["route"]
            children = model_check["children"]
            assert type(is_leaf) is bool
            assert type(route) is str
            assert type(children) is list
            for check in children:
                assert type(check) is dict
                if check["is_leaf"] == True:
                    print("is_leaf")
                    response_test = client.post(
                        f"{base_route}/inspect_file",
                        data={
                            "object": "BRep",
                            "filename": "corbi.og_brep",
                            "test": check["route"],
                        },
                    )

                    assert response_test.status_code == 200
                else:
                    print("not is_leaf")


def test_inspect_file(client):
    # Test with file
    response = client.post(
        f"{base_route}/inspect_file",
        data={
            "file": base64.b64encode(open("./tests/data/test.og_brep", "rb").read()),
            "filename": "corbi.og_brep",
            "filesize": os.path.getsize("./tests/data/test.og_brep"),
        },
    )
