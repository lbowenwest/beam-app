var path = require('path');
var webpack = require('webpack');

var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var rootAssetPath = path.join(__dirname, 'client');


module.exports = {
    entry: {
        vendor: [],

        app: path.join(rootAssetPath, 'app'),
        site: path.join(rootAssetPath, 'site')
    },
    output: {
        path: path.resolve(__dirname, 'build'),
        publicPath: 'http://localhost:8080/assets/',
        filename: '[name].bundle.js',
        chunkFilename: '[id].bundle.js'
    },
    resolve: {
        extensions: ['', '.jsx', '.js', '.scss', '.css']
    },
    resolveLoader: {
        root: path.join(__dirname, 'node_modules')
    },

    plugins: [
        new ExtractTextPlugin('[name].bundle.css'),
        new ManifestRevisionPlugin(path.join('build', 'manifest.json'), {
            rootAssetPath: path.join('client')
        }),
        new webpack.optimize.CommonsChunkPlugin({
            name: 'vendor',
            filename: 'vendor.bundle.js',
            minChunks: 2
        })
    ],

    module: {
        loaders: [{
            test: /\.js/,
            exclude: /node_modules/,
            loader: 'babel-loader'
        }, {
            test: /\.(sc|sa|c)ss/,
            loader: ExtractTextPlugin.extract('style-loader', 'css-loader!sass'),
        }, {
            test: /\.json$/,
            loader: 'json-loader'
        }, {
            test: /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
            loader: "url?limit=10000"
        }, {
            test: /\.(ttf|eot|svg)(\?[\s\S]+)?$/,
            loader: 'file'
        }]
    }
};

