# Sihc Library: CQRS pattern with asyncio python

This is my own library. It's coded by me from 13/07/2020.

This library base on CQRS model that I split out the API server and Query server.

I'll update example soon (when I have time) but it's worked now.

## I. API server

### I.1. Main idea

Definitions:

#### [Model](#model)

This is a [sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/) model. But since this is an asyncio python, so I used the [gino](https://python-gino.org/docs/en/master/tutorials/tutorial.html) model (partly in `sqlalchemy`) instead.

#### [Resource](#resource)

It represents a [model](#model).  
It is not only the only way to connect to the Model, but also a two-way validator: before you push data to the database and when you pull data from the database.

#### [Datadef](#datadef)

Data definition is a class that inherits from the [PClass](https://pyrsistent.readthedocs.io/en/latest/api.html#pyrsistent.PClass) to specify the input data. It will raise an exception if the input data is missing or incorrect type.

#### [Entity](#entity)

This looks like a key in a hash table. This key not only helps you connect to the function you need, but also validates the input before that function runs. So the error will appear before entering the function and you will easily know what the problem is.

#### [Command](#command)

- Command Entity: This is how the client executes a command (passes it on the URL). And it validates the input.
- Command Handler: This function is connected with one or some command entities and called when these entity called. This function return some event and response.

#### [Event](#event)

- Event Entity: This cannot be invoked by the client, just by the command handler. And validate input data
- Event Handler: This function is connected with one or some event entities and called when these entity called. This function return some mutation.

#### [Response](#response)

- Response Entity: ...
- Response Handler: return json, file stream, etc ...

#### [Mutation](#mutation)

It creates the `INSERT` query, `UPDATE` query and optimized query. It isn't excute anything.

#### [State Manager](#statemgr)

This `State Manager` store:
- All item get from DB.
- The new and modified items.
- All mutations and excuted it.

And then, update it to the Database.

Pros:
- Easy way to cache the data.
- We store every items in `State Manager` because for each item, we only need to query and update once on the Database. The latest version of the item is saved and managed by `State Manager`.
- We can do some work on `State` as automatically set the `time created`, `time updated`, `time deleted`, `creator`, `updater`, `etag`.
- It can solve the problem of multiple users modifying an object on the database at the same time (using a combination of identifier and etag).
- Its runing processes (database updates) can be deferred (ignored) and wait until another database updates have finished. It can be seen as a local database.

#### [Domain](#domain)

The domain definition used to separate the [Resources](#resource) that a domain can connect to.

This is the most important definition. It connects all previous sections together:
- Connect `Command Entity` with `Command Handler`
- Connect `Event Entity` with `Event Handler`
- Connect `Command` to `Event` and `Response`
- Give the way to connect to `Resource`

You can run multiple domains at the same time with no conflicts. Each domain can be an application.
