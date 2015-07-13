React/Python examples
=====================

- [python-webpack examples](https://github.com/markfinger/python-webpack/tree/master/examples)
- [django-webpack-loader examples](https://github.com/owais/django-webpack-loader/tree/master/examples)

Illustrates how to use webpack so that you can integrate your React components into the frontend of a python system.

--------------------------------------

[Basic rendering](basic_rendering)

Illustrates how to pre-render React components for a production system. The example use React as a substitute for 
python template systems.

--------------------------------------

[Self mounting components](self_mounting_components)

Illustrates a workflow where webpack is used to generate bundles of your components with self mounting code. The 
bundles will immediately mount themselves over the pre-rendered markup as soon as the page has loaded the JS.

This workflow is similar to what was provided in older versions of python-react. It can be useful
if you want to add a small amount of interactivity to an otherwise backend-heavy site.

Be aware that while this workflow can be initially convenient, it tends to rely on components maintaining
large amounts of state. A better workflow is for your components to minimize state by delegating all
data storage to external services. If you're looking for something to handle your data, the multitude
of Flux implementations are a reasonable starting point.

--------------------------------------

*Feel free to open a pull request, if you'd like to contribute more examples or links*
