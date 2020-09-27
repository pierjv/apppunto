#from google.cloud import datastore
from src.controllers.responseController import responseController

class uploadController(responseController):
        
    def get(self):
        # Instantiates a client
        return 'OK'
    '''print('1')
    datastore_client = datastore.Client()

    # The kind for the new entity
    kind = 'Task'
    # The name/ID for the new entity
    name = 'sampletask10110111'
    # The Cloud Datastore key for the new entity
    print('1.1')
    task_key = datastore_client.key(kind, name)
    print(task_key)
    # Prepares the new entity
    task = datastore.Entity(key=task_key)
    task['description'] = 'Jean Pierre'

    # Saves the entity
    datastore_client.put(task)
    print(task.key)
    print('Saved {}: {}'.format(task.key.name, task['description']))
    print(datastore_client.get(key=task_key))'''

    '''def implicit(self):
        # If you don't specify credentials when constructing the client, the
        # client library will look for credentials in the environment.
        storage_client = datastore.Client()
        print(storage_client)
        print(dir(storage_client))
        
        # Make an authenticated API request
        buckets = list(storage_client.list_buckets())

        print(buckets)'''

    ''' """Import the data for this recipe by either saving the image associated
    with this recipe or saving the metadata associated with the recipe. If
    the metadata is being processed, the title and description of the recipe
    must always be specified."""
    try:
        if 'recipe_image' in request.files:
            filename = images.save(request.files['recipe_image'])
            self.image_filename = filename
            self.image_url = images.url(filename)
        else:
            json_data = request.get_json()
            self.recipe_title = json_data['title']
            self.recipe_description = json_data['description']
            if 'recipe_type' in json_data:
                self.recipe_type = json_data['recipe_type']
            if 'rating' in json_data:
                self.rating = json_data['rating']
            if 'ingredients' in json_data:
                self.ingredients = json_data['ingredients']
            if 'recipe_steps' in json_data:
                self.recipe_steps = json_data['recipe_steps']
            if 'inspiration' in json_data:
                self.inspiration = json_data['inspiration']
    except KeyError as e:
        raise ValidationError('Invalid recipe: missing ' + e.args[0])
    return self

    @recipes_api_blueprint.route('/api/v1_2/recipes/<int:recipe_id>', methods=['PUT'])
    def api1_2_update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe.import_data(request)
    db.session.add(recipe)
    db.session.commit()'''
    