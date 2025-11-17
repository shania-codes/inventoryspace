# Inventory Space
> Clear your mental space by organising your physical space.

Inventory Space is an offline inventory space management system designed to help users free up mental space by digitally storing what they own and where it is. 

When users store items they can also add custom attributes (ex: date_purchased: "10.11.2025") and tags (ex: kitchen_equipment, groceries, spare_parts, cables, etc.) they can manage their whole house easily. [Not Implemented]

It also has a self hosted API for integration with other programs. For example, custom user defined recipes that use the details of their saved groceries and kitchen equipment to know if they can make that recipe or not, and to then automatically add it to their food diary including it's calories and macronutrient information and automatically decrement the amount of the item left in their inventory OR automatically add it to their shopping list (such as by using attributes: store, price, servings per item). [Not Implemented]

It runs without internet access. It doesn't need an account or have any ads or require a cloud server to work. Everything is stored locally in a SQLite3 database.


## Features
- Home screen / Dashboard page (only one item for now)
- Add items to "No Location"
- All data is stored locally offline, no internet access required
### Planned Features
- Add new location 
- Add tags to items
- Add attributes to items
- When adding a tag add attributes, for example a food tag automatically adds attributes opened_data and expiry_date or calories and macronutrients attributes.
- Universal item storage, store any item with a name, description, and custom attributes (ex: date_purchased:"10.11.2025", expiry_date"23.11.2025", calories:200)
- Tag system, assign custom tags (ex: groceries, kitchen_equipment, spare_parts, cables)
- API can be used seperately by other programs such as a recipe "app", food diary "app" and shopping list generator "app".

## Resources
- https://python-gtk-3-tutorial.readthedocs.io/en/latest/
- https://docs.python.org/3/library/sqlite3.html#sqlite3-tutorial

## License
Licensed under the GNU General Public License v3.0 (GPLv3).