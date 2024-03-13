# Send to Telegram

The **fetch_structures** Sequence retrieves structures with `height>50m` from OpenStreetMap using **[Overpass interpreter](https://overpass-api.de/)**.  
The **transform_xml** Sequence takes the fetched data as an input and truncates all tags except for: *coordinates, height* and *building type*.

Data is exchanged using `structures-xml` Topic with content-type `text/plain`.

___


## Running
> 💡**NOTE:** Packaging of Python Sequences is not very "pythonic" for now. If you have any idea, how we should resolve it for your comfort, please let us know [here](https://github.com/scramjetorg/transform-hub/issues/598).

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/transform-hub/installation) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

Open the terminal and run the following commands:

```bash
# Install dependencies
npm run build

# Deploy samples to Hub
npm run deploy:fetch
npm run deploy:transform
```

To get it going, input 4 coordinates to fetch_structures Sequence:  
*Min Latitude, Min Longitude, Max Latitude, Max Longitude*  
  
Fifth argument, *height*, is optional and **50** by default.
```bash
si inst input <instance-id>
# type in e.g. 52.1485 20.7917 52.3667 21.2816 80
#  Warsaw buildings with height>80m
```
>You can get the coordinates using **[bbox tool](https://norbertrenner.de/osm/bbox.html)** 🔧.

You can also
Data will then be fetched and passed to the Topic.  

The **transform_xml** Sequence will parse the xml file from the Topic and remove unnecessary tags.  
You can edit the `transform_xml/main.py` to save the result xml into e.g. database. 
```py
    xml_file = transform_xml_data(''.join(chunks))
    context.logger.info('Transformed xml file')
    # save to e.g. database...
```
___


