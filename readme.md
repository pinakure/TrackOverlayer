<img style="display:inline-block" src="https://github.com/pinakure/yt-obs/blob/main/doc/icon.png?raw=true" width="64" height="64"/>
<table style="border: none !important; width:100%;">
    <tr>
        <td><h3>tRAckOverlayer</h3></td>
    <tr>
    </tr>
    <tr>
         <td><h4>A retroachievement user data tracker who likes overlays too much</h4></td>
    </tr>
    <tr>
        <td>
        This is a tool used to keep track of the user data like game progress, current game, global score, number of cheevos unlocked, etc.
After retrieving the data, it presents to the user a comprehensive list of cheevos corresponding to the game the user is actually playing
and allows him to choose an achievement to be 'the target'.<br/>
The tool will generate a custom overlay HTML file onto which each one of the different displayable elements will be inserted at their corresponding position,
with customizable parameters and styles which can be modified using CSS or tweaking them in the preferences menu.
        </td>
    </tr>
         <td>
            <img style="display:inline-block" src="https://github.com/pinakure/yt-obs/blob/main/doc/interface.png?raw=true" width="1044" height="1343"/>
        </td>
    </tr>
<table>
<h4>How to Install</h4>
<a href="https://raw.githubusercontent.com/pinakure/yt-obs/main/doc/how-to-install.svg">Open installation flow chart</a>

<h4>Getting started</h4>
<a href="">Open getting started flow chart</a>

<h4>Plugins</h4>
<p>Each of the elements displayed in the overlay are generated by a plugin.</p><p>A plugin consists, at less, on two files:</p>
<ul>
<li>plugin.py     - Contains the properties and methods of the plugin.</li>
<li><a href="https://github.com/pinakure/yt-obs/blob/main/ramon/plugins/example.html">template.html</a> - Contains the frontend structure for the plugin. </li>
