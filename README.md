# AirBnB Clone - v2

## Description
Second phase of the AirBnB clone project. It adds MySQL storage with
SQLAlchemy (`DBStorage`) next to the JSON file storage (`FileStorage`),
object creation with parameters from the console, and unit tests.

## Storage engines
| Engine | How to select |
|--------|---------------|
| FileStorage (default) | no environment variable needed, data in `file.json` |
| DBStorage (MySQL) | `HBNB_TYPE_STORAGE=db` plus the variables below |

Environment variables for DBStorage: `HBNB_MYSQL_USER`, `HBNB_MYSQL_PWD`,
`HBNB_MYSQL_HOST`, `HBNB_MYSQL_DB`, and `HBNB_ENV` (`test` drops all tables
at start).

Prepare MySQL (needs the `mysqlclient` and `SQLAlchemy` packages):
```bash
cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p
cat setup_mysql_test.sql | mysql -hlocalhost -uroot -p
```

## Command interpreter
### How to start
```bash
./console.py
```
or, with MySQL:
```bash
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost \
HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db ./console.py
```

### Commands
| Command | Description |
|---------|-------------|
| `create <Class> <key>=<value> ...` | Create an object. Strings in double quotes (`_` becomes a space), integers `42`, floats `3.14` |
| `show <Class> <id>` | Print one object |
| `destroy <Class> <id>` | Delete one object |
| `all [<Class>]` | Print all objects (or all of one class) |
| `count <Class>` | Count the objects of a class |
| `update <Class> <id> <attribute> <value>` | Update one attribute |
| `<Class>.all()`, `.count()`, `.show(id)`, `.destroy(id)`, `.update(id, attr, value)` | Same commands, dotted form |
| `quit` / `EOF` | Exit |

### Example
```
(hbnb) create State name="California"
(hbnb) create Place city_id="<id>" user_id="<id>" name="My_little_house" number_rooms=4 latitude=37.77
```

## Models
`User`, `State`, `City`, `Amenity`, `Place`, `Review` (all inherit from
`BaseModel`). `Place` and `Amenity` are linked many-to-many through the
`place_amenity` table.

## Tests
```bash
python3 -m unittest discover tests
```
