const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
    entry: './src/index.tsx',
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: [
                    {loader: 'ts-loader'}
                ],
                exclude: /node_modules/,
            },
        ],
    },
    resolve: {
        fallback: {
            "buffer": require.resolve("buffer/"),
            "path": false,
            "fs": false,
            "assert": false,
            "stream": false,
        },
        extensions: ['.tsx', '.ts', '.js'],
    },
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, '../src/evidently/nbextension/static/'),
    },
    optimization: {
        minimize: true,
        minimizer: [
            new TerserPlugin({
                terserOptions: {
                    output: {
                        comments: false,
                    },
                },
            }),
        ],
    },
};