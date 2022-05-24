"""Defines the REST API.
"""

from typing import Callable
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import Schema, fields
import marshmallow


class ErrorSchema(Schema):
    message = fields.Str(required=True)
    type = fields.Str()
    identifier = fields.Str()


class JobInfoSchema(Schema):
    job_id = fields.Str(required=True)


class JobInputSchema(Schema):
    execute_arguments = fields.Mapping()
    worker_options = fields.Mapping()


class ResourceIdentifierSchema(Schema):
    identifier = fields.Str(required=True)


class ResourceIdentifierListSchema(Schema):
    identifiers = fields.List(fields.Str, required=True)


class EwoksGraphSchema(Schema):
    graph = fields.Mapping()
    nodes = fields.List(fields.Mapping)
    links = fields.List(fields.Mapping)

class EwoksIconBinarySchema(Schema):
    file = marshmallow.fields.Raw(type='file')

class EwoksTaskSchema(Schema):
    task_type = fields.Str(required=True)
    task_identifier = fields.Str(required=True)
    category = fields.Str()
    icon = fields.Str()
    required_input_names = fields.List(fields.Str)
    optional_input_names = fields.List(fields.Str)
    output_names = fields.List(fields.Str)


class EwoksGraphListSchema(Schema):
    items = fields.List(fields.Nested(EwoksGraphSchema()))


class EwoksTaskListSchema(Schema):
    items = fields.List(fields.Nested(EwoksTaskSchema()))


class DiscoverSchema(Schema):
    modules = fields.List(fields.Str)


def get_resource_content_schema(resource_type: str):
    if resource_type == "workflow":
        return EwoksGraphSchema
    elif resource_type == "task":
        return EwoksTaskSchema
    elif resource_type == "icon":
        return EwoksIconBinarySchema
    else:
        raise TypeError(resource_type)


def get_resource_content_list_schema(resource_type: str):
    if resource_type == "workflow":
        return EwoksGraphListSchema
    elif resource_type == "task":
        return EwoksTaskListSchema
    else:
        raise TypeError(resource_type)


def get_resource(resource_type: str):
    def wrapper(func: Callable):
        bodyschema = get_resource_content_schema(resource_type)
        func = doc(summary=f"Get a {resource_type} as JSON")(func)
        func = marshal_with(
            bodyschema,
            code=200,
            description=f"{resource_type} in JSON format",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=403,
            description=f"no permission to read the {resource_type}",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=404,
            description=f"requested {resource_type} is not found",
        )(func)
        return func

    return wrapper

def get_resource_binary(resource_type: str):
    def wrapper(func: Callable):
        bodyschema = get_resource_content_schema(resource_type)
        func = doc(summary=f"Get an {resource_type} as Binary")(func)
        func = marshal_with(
            bodyschema,
            code=200,
            description=f"{resource_type} in binary format",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=403,
            description=f"no permission to read the {resource_type}",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=404,
            description=f"requested {resource_type} is not found",
        )(func)
        return func

    return wrapper


def put_resource(resource_type: str):
    def wrapper(func: Callable):
        bodyschema = get_resource_content_schema(resource_type)
        func = doc(summary=f"Update a {resource_type} from JSON")(func)
        func = use_kwargs(bodyschema)(func)
        func = marshal_with(
            bodyschema,
            code=200,
            description=f"{resource_type} was overwritten",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=400,
            description=f"bad {resource_type} update request",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=403,
            description=f"no permission to write the {resource_type}",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=404,
            description=f"requested {resource_type} is not found",
        )(func)
        return func

    return wrapper


def post_resource(resource_type: str):
    def wrapper(func: Callable):
        bodyschema = get_resource_content_schema(resource_type)
        func = doc(summary=f"Create a {resource_type} from JSON")(func)
        func = use_kwargs(bodyschema)(func)
        func = marshal_with(
            bodyschema,
            code=200,
            description=f"{resource_type} in JSON format",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=400,
            description=f"bad {resource_type} create request",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=403,
            description=f"no permission to write the {resource_type}",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=409,
            description=f"requested {resource_type} already exists",
        )(func)
        return func

    return wrapper

def upload_resource(resource_type: str):
    def wrapper(func: Callable):
        bodyschema = get_resource_content_schema(resource_type)
        func = doc(summary=f"Upload an {resource_type} in Binary format")(func)
        func = use_kwargs(bodyschema)(func)
        func = marshal_with(
            bodyschema,
            code=200,
            description=f"{resource_type} in Binary format",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=400,
            description=f"bad {resource_type} upload request",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=403,
            description=f"no permission to write the {resource_type}",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=409,
            description=f"requested {resource_type} already exists",
        )(func)
        return func

    return wrapper


def delete_resource(resource_type: str):
    def wrapper(func: Callable):
        func = doc(summary=f"Delete a {resource_type}")(func)
        func = marshal_with(
            ResourceIdentifierSchema,
            code=200,
            description=f"{resource_type} has been removed or did not exist",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=403,
            description=f"no permission to delete the {resource_type}",
        )(func)
        return func

    return wrapper


def list_resource_identifiers(resource_type: str):
    def wrapper(func: Callable):
        func = doc(summary=f"Get a list of {resource_type} identifiers")(func)
        func = marshal_with(ResourceIdentifierListSchema, code=200)(func)
        return func

    return wrapper


def list_resource_content(resource_type: str):
    def wrapper(func: Callable):
        func = doc(summary=f"Get a list of {resource_type}s")(func)
        func = marshal_with(get_resource_content_list_schema(resource_type), code=200)(
            func
        )
        return func

    return wrapper


def execute_resource(resource_type: str):
    def wrapper(func: Callable):
        func = doc(summary=f"Start {resource_type} execution")(func)
        func = use_kwargs(JobInputSchema)(func)
        func = marshal_with(
            JobInfoSchema,
            code=200,
            description=f"{resource_type} execution started",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=403,
            description=f"no permission to read the {resource_type}",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=404,
            description=f"requested {resource_type} is not found",
        )(func)
        return func

    return wrapper


def discover_resources(resource_type: str):
    def wrapper(func: Callable):
        func = doc(summary=f"Discover {resource_type}s")(func)
        func = use_kwargs(DiscoverSchema)(func)
        func = marshal_with(ResourceIdentifierListSchema, code=200)(func)
        func = marshal_with(
            ErrorSchema,
            code=403,
            description=f"no permission to write the {resource_type}",
        )(func)
        func = marshal_with(
            ErrorSchema,
            code=409,
            description=f"requested {resource_type} already exists",
        )(func)
        return func

    return wrapper
