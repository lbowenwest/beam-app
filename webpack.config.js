var path = require('path');
var webpack = require('webpack');

var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');
// var ExtractTextPlugin = require('extract-text-webpack-plugin');

var rootAssetPath = path.join(__dirname, 'client');


module.exports = {
    entry: {
        vendor: ['jquery', 'react', 'react-router', 'react-dom'],
        app: path.join(rootAssetPath, 'src', 'index.js'),
        style: path.join(rootAssetPath, 'sass', 'index.scss')
    },
    output: {
        path: path.resolve(__dirname, 'build'),
        publicPath: '/assets/',
        filename: '[name].bundle.js',
        chunkFilename: '[id].bundle.js'
    },
    resolve: {
        extensions: ['', '.js', '.scss', '.css']
    },
    resolveLoader: {
        root: path.join(__dirname, 'node_modules')
    },

    plugins: [
        // new ExtractTextPlugin('style.bundle.css'),
        new ManifestRevisionPlugin(path.join('build', 'manifest.json'), {
            rootAssetPath: path.join('client'),
            ignorePaths: ['sass', 'src', 'dist']
        }),
        new webpack.optimize.CommonsChunkPlugin({
            name: 'vendor',
            filename: 'vendor.bundle.js',
            minChunks: Infinity
        })
    ],

    module: {
        loaders: [{
            test: /\.js/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            include: [
                path.join(rootAssetPath, 'src')
            ]
        }, {
            test: /\.scss/,
            // loader: ExtractTextPlugin.extract('style', 'css', 'sass'),
            loaders: ['style', 'css', 'sass'],
            include: [
                path.join(rootAssetPath, 'sass')
            ]
        }, {
            test: /\.json$/,
            loader: 'json-loader'
        }]
    }
};

