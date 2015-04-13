BUNDLE_CONFIG = \
"""module.exports = {{
    context: '{dir}',
    entry: '{file}',
    output: {{
        path: '[bundle_dir]/react-components',
        filename: '{var}-[hash].js',
        libraryTarget: 'umd',
        library: '{var}'
    }},
    externals: [{{
      'react': {{
        commonjs2: '{path_to_react}',
        root: 'React'
      }}
    }}],
    devtool: 'eval'{translate_config}
}};
"""

BUNDLE_TRANSLATE_CONFIG = \
""",
    module: {{
        loaders: [{{
            test: /\{ext}$/,
            exclude: /node_modules/,
            loader: 'babel-loader'
        }}]
    }},
    resolveLoader: {{
        root: '{node_modules}'
    }}
"""