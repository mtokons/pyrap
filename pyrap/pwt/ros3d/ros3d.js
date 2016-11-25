pwt_ros3d = {};

pwt_ros3d.Simulation = function(parent, cssid, url, port) {
    this._urdfnodeDiv = this.createElement(parent);
    this._w = 800;
    this._h = 600;

    this._urdfnodeDiv.setAttribute('id', cssid ? cssid : 'urdf');
    this._rosliburl = url ? url : 'ws://prac.open-ease.org';
    this._roslibport = port ? port : '9090';

    this._needsLayout = true;
    this._needsRender = true;
    var that = this;
    rap.on( "render", function() {
        if( that._needsRender ) {
            if( that._needsLayout ) {
                that.init( that );
                that._needsLayout = false;
            }
            that._needsRender = false;
        }
    } );
    parent.addListener( 'Resize', function() {
        that.setBounds( parent.getClientArea() );
    } );
    this.setBounds( parent.getClientArea() );

};

pwt_ros3d.Simulation.prototype = {

    createElement: function( parent ) {
        var clientarea = parent.getClientArea();
        var element = document.createElement( 'div' );
        element.style.position = 'absolute';
        element.style.left = clientarea[0];
        element.style.top = clientarea[1];
        parent.append( element );
        return element;
    },

    setZIndex : function(index) {
        this._urdfnodeDiv.style.zIndex = index;
    },

    setBounds: function( args ) {
        this._urdfnodeDiv.style.left = args[0] + 'px';
        this._urdfnodeDiv.style.top = args[1] + 'px';
        this._urdfnodeDiv.style.width = args[2] + 'px';
        this._urdfnodeDiv.style.height = args[3] + 'px';
        if (typeof this._simulation_viewer != 'undefined') {
            this._simulation_viewer.resize(args[2], args[3]);
        }
     },

    destroy: function() {
        var element = this._urdfnodeDiv;
        if( element.parentNode ) {
            element.parentNode.removeChild( element );
        }
    },

    setWidth: function( width ) {
        this._w = width;
        this._simulation_viewer.style.width = width;
    },

    setHeight: function( height ) {
        this._h = height;
        this._simulation_viewer.style.height = height;
    },

    setURL: function( url ) {
        this._rosliburl = url;
    },

    setPort: function ( port ) {
        this._roslibport = port;
    },

    init: function() {

        // remove all content from earlier simulations
        while (this._urdfnodeDiv.firstChild) {
            this._urdfnodeDiv.removeChild(this._urdfnodeDiv.firstChild);
        }

        // Connect to ROS.
        var ros = new ROSLIB.Ros({
          url : this._rosliburl + ':' + this._roslibport
        });

        // Create the main viewer.
        this._simulation_viewer = new ROS3D.Viewer({
          divID : this._urdfnodeDiv.attributes.id.value,
          width : this._w,
          height : this._h,
          antialias : true,
          cameraPose : new THREE.Vector3(-3, 3, 3)
        });

        // Add a grid.
        this._simulation_viewer.addObject(new ROS3D.Grid());

        // Setup a client to listen to TFs.
        var tfClient = new ROSLIB.TFClient({
          ros : ros,
          fixedFrame : 'map',
          angularThres : 0.01,
          transThres : 0.01,
          rate : 10.0
        });

        // Setup the marker client.
        var markerClient = new ROS3D.MarkerClient({
          ros : ros,
          tfClient : tfClient,
          topic : '/visualization_marker',
          path : 'http://svn.ai.uni-bremen.de/svn/sim_models/',
          rootObject : this._simulation_viewer.scene
        });

        // Setup the URDF client.
        var urdfClient = new ROS3D.UrdfClient({
          ros : ros,
          tfClient : tfClient,
          param : 'robot_description_nocol',
          path : 'http://svn.ai.uni-bremen.de/svn/sim_models/',
          rootObject : this._simulation_viewer.scene,
          loader : ROS3D.COLLADA_LOADER
        });

        var urdfClient2 = new ROS3D.UrdfClient({
          ros : ros,
          tfClient : tfClient,
          param : 'kitchen_description',
          tfPrefix : 'iai_kitchen',
          path : 'http://svn.ai.uni-bremen.de/svn/sim_models/',
          rootObject : this._simulation_viewer.scene,
          loader : ROS3D.COLLADA_LOADER
        });

    /**/
        var urdfClient3 = new ROS3D.UrdfClient({
          ros : ros,
          tfClient : tfClient,
          param : 'pizza_description',
          path : 'http://svn.ai.uni-bremen.de/svn/sim_models/',
          rootObject : this._simulation_viewer.scene,
          loader : ROS3D.COLLADA_LOADER
        });

        var urdfClient4 = new ROS3D.UrdfClient({
          ros : ros,
          tfClient : tfClient,
          param : 'cutter_description',
          path : 'http://svn.ai.uni-bremen.de/svn/sim_models/',
          rootObject : this._simulation_viewer.scene,
          loader : ROS3D.COLLADA_LOADER
        });

        var urdfClient5 = new ROS3D.UrdfClient({
          ros : ros,
          tfClient : tfClient,
          param : 'bread_description',
          path : 'http://svn.ai.uni-bremen.de/svn/sim_models/',
          rootObject : this._simulation_viewer.scene,
          loader : ROS3D.COLLADA_LOADER
        });

        var urdfClient6 = new ROS3D.UrdfClient({
          ros : ros,
          tfClient : tfClient,
          param : 'knife_description',
          path : 'http://svn.ai.uni-bremen.de/svn/sim_models/',
          rootObject : this._simulation_viewer.scene,
          loader : ROS3D.COLLADA_LOADER
        });
    }

};

// Type handler
rap.registerTypeHandler( 'pwt.customs.ROS3D', {

  factory: function( properties ) {
    var parent = rap.getObject( properties.parent );
    return new pwt_ros3d.Simulation( parent, properties.cssid, properties.url, properties.port);
  },

  destructor: 'destroy',

  properties: [ 'remove', 'bounds', 'port', 'url', 'width', 'height'],

  methods : [ ],

  events: [ ]

} );