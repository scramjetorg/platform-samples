# pokemon

___

In this sample we use open API from <https://pokeapi.co>. Pokemon name will be passed into the instance's input, then a request is sent to the API. The returned data is saved to the instance `stdout` endpoint, and the weight of the pokemon whose name was given in input is returned to the output of the instance.

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/platform/self-hosted-installation) or use the [platform's environment](https://docs.scramjet.org/platform/quick-start) for the sequence deployment.

Open two terminals and run the following commands:

**The first terminal:**

```bash
# go to 'pokemon' directory
cd javascript/pokemon

# install dependencies
npm install

# go back to javascript/ directory
cd ../

# deploy 'pokemon' Sequence
si seq deploy pokemon

# see the Instance output
si inst output -    # nothing happens until some data is sent to input
```

> 💡**NOTE:** Command `deploy` performs three actions at once: `pack`, `send` and `start` the Sequence. It is the same as if you would run those three commands separately:

```bash
si seq pack . -o pokemon.tar.gz    # compress 'pokemon/' directory into file named 'pokemon.tar.gz'

si seq send pokemon.tar.gz    # send compressed Sequence to STH, this will output Sequence ID

si seq start -    # start the Sequence, this will output Instance ID
```

**The second terminal**

```bash
# send pokemon name as instance input which will be read from stdin
si inst input -
# hit enter and type any pokemon name, eg. pikachu
pikachu
# hit enter and check out the terminal that reads the output endpoint
```

## Output and stdout

As an instance output you should see the weight of the pokemon send in the input stream:

```js
$ si inst output -
6
```

There is also some pokemon data piped to `stdout` endpoint:

```bash
si inst stdout -
```

```bash
{
  abilities: [
    { ability: [Object], is_hidden: false, slot: 1 },
    { ability: [Object], is_hidden: true, slot: 3 }
  ],
  base_experience: 112,
  forms: [
    {
      name: 'pikachu',
      url: 'https://pokeapi.co/api/v2/pokemon-form/25/'
    }
  ],
  game_indices: [
    { game_index: 84, version: [Object] },
    { game_index: 25, version: [Object] }
  ],
  height: 4,
  held_items: [
    { item: [Object], version_details: [Array] },
    { item: [Object], version_details: [Array] }
  ],
  id: 25,
  is_default: true,
  location_area_encounters: 'https://pokeapi.co/api/v2/pokemon/25/encounters',
  moves: [
    { move: [Object], version_group_details: [Array] },
    { move: [Object], version_group_details: [Array] }
  ],
  name: 'pikachu',
  order: 35,
  past_types: [],
  species: {
    name: 'pikachu',
    url: 'https://pokeapi.co/api/v2/pokemon-species/25/'
  },
  sprites: {
    back_default: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/25.png',
    back_female: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/female/25.png',
    back_shiny: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/25.png',
    back_shiny_female: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/female/25.png',
    front_default: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png',
    front_female: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/female/25.png',
    front_shiny: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/25.png',
    front_shiny_female: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/female/25.png',
    other: {
      dream_world: [Object],
      home: [Object],
      'official-artwork': [Object]
    },
    versions: {
      'generation-i': [Object],
      'generation-ii': [Object],
      'generation-iii': [Object],
      'generation-iv': [Object],
      'generation-v': [Object],
      'generation-vi': [Object],
      'generation-vii': [Object],
      'generation-viii': [Object]
    }
  },
  stats: [
    { base_stat: 35, effort: 0, stat: [Object] },
    { base_stat: 55, effort: 0, stat: [Object] },
    { base_stat: 40, effort: 0, stat: [Object] },
    { base_stat: 50, effort: 0, stat: [Object] },
    { base_stat: 50, effort: 0, stat: [Object] },
    { base_stat: 90, effort: 2, stat: [Object] }
  ],
  types: [ { slot: 1, type: [Object] } ],
  weight: 60
}
```
