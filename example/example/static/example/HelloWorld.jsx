/**
 * Begin by naming your bridge module the same as the component name
 * in your `ReactComponent` subclass.
 *
 * Then, require React itself.
 *
 * When mounting a React component into a Django page using django-react,
 * the component and its module act as a "bridge"
 * between rendering of the component on the server
 * and mounting and lifecycle management of the component on the client.
 *
 * In a typical project, you'd also require subcomponents here,
 * and any other packages that your bridge module needs
 * to successfully render on the server and manage lifecycle on the client.
 */
var React = require('react');


/**
 * django-react produces code to initialize such bridge components,
 * and needs access to React in order to do so.
 *
 * React is bundled with your component during the build process,
 * so the bridge component's module needs to expose React.
 *
 * When rendering on the server, `window` doesn't exist,
 * so we check for its existence first before setting it.
 */
if (typeof window !== 'undefined') { window.React = React; }


/**
 * Create your bridge component as you would any other React component.
 */
var HelloWorld = React.createClass({

    render: function() {

        /**
         * On the server side, props will be set to the values you provided
         * when instantiating the component in Python.
         *
         * On the client side, props will be set to those same values,
         * as they will have been serialized, and sent to the client
         * along with initialization code via `{{ component.render_js }}`
         *
         * See also `example.views.index` Python module,
         * and `example/index.html` Django template.
         */
        return <span>Hello, {this.props.name}!</span>;

    },

    componentDidMount: function() {

        /**
         * Until django-react is refactored to allow for more flexiblity,
         * you can use `componentDidMount` in your bridge component
         * to kick off client-side lifecycle management for the component.
         *
         * In this example, we are going to wait 5 seconds,
         * then change our `name` prop to be uppercase,
         * and finally force an update.
         *
         * This will occur on the client side, but not the server,
         * so the visual effect will be "Hello, World!"
         * followed by "Hello, WORLD!", given that `name == 'World'`.
         */

        /**
         * NOTE: This is a contrived example, and you should NOT use
         * setTimeout, props, or forceUpdate in this fashion.
         * This was just a simple way to demonstrate
         * server-side vs client-side component lifecycle.
         */

        setTimeout(function () {
            this.props.name = this.props.name.toUpperCase();
            this.forceUpdate();
        }.bind(this), 5000);

    }

});

module.exports = HelloWorld;