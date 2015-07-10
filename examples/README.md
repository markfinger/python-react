React/Python examples
=====================

[Basic rendering](basic_rendering)

Illustrates how to pre-render React components from python. It illustrates how to use React as a
substitute for python template layers.

--------------------------------------

[python-webpack examples](https://github.com/markfinger/python-webpack/tree/master/examples)

Illustrates how to use python-webpack to integrate React assets into a python system.

--------------------------------------

[Self mounting components](self_mounting_components)

Illustrates a workflow where webpack is used to generate bundles so that the root React component
can immediately mount itself over the markup that was pre-rendered with the same data.

This workflow is similar to what was provided in older versions of python-react. It can be useful
if you want to add interactivity to an otherwise backend-heavy site.

Be aware that while this workflow can be initially convenient, it tends to rely on components maintaining
large amounts of state. A better workflow is for your components to minimize state by delegating all
data storage to external services. If you're looking for something to handle your data, the multitude
of Flux implementations are a reasonable starting point.

--------------------------------------

*Feel free to open a pull request, if you'd like to contribute more examples or links*