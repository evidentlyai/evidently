const path = require('path');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
    entry: './src/index.tsx',
    // devtool: 'source-map',
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
            "fs": false
        },
        extensions: ['.tsx', '.ts', '.js'],
    },
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, '../src/evidently/nbextension/static/'),
        clean: true,
    },
    plugins: [
        new BundleAnalyzerPlugin({analyzerPort: 7000})
    ]
};