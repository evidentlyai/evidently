import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import typescript from "@rollup/plugin-typescript";
import json from "@rollup/plugin-json";
import glob from "glob";
import path from "node:path";
import { fileURLToPath } from "node:url";
import dts from "rollup-plugin-dts";
import { terser } from "rollup-plugin-terser";
import peerDepsExternal from "rollup-plugin-peer-deps-external";

const packageJson = require("./package.json");

export default [
  {
    input: Object.fromEntries(
		glob.sync('src/**/*.ts*').map(file => [
			// This remove `src/` as well as the file extension from each
			// file, so e.g. src/nested/foo.js becomes nested/foo
			path.relative(
				'src',
				file.slice(0, file.length - path.extname(file).length)
			),
			// This expands the relative paths to absolute paths, so e.g.
			// src/nested/foo becomes /project/src/nested/foo.js
			fileURLToPath(new URL(file, import.meta.url))
		])
	),
    output: [
      {
        dir: ".",
        format: "cjs",
        sourcemap: true,
      }
    ],
    plugins: [
      peerDepsExternal(),
      commonjs(),
      typescript({ tsconfig: "./tsconfig.json" }),
      terser(),
    ],
    external: ["react", "react-dom", "styled-components"],
  },
  {
    input: Object.fromEntries(
		glob.sync('src/**/*.ts*').map(file => [
			// This remove `src/` as well as the file extension from each
			// file, so e.g. src/nested/foo.js becomes nested/foo
			path.relative(
				'src',
				file.slice(0, file.length - path.extname(file).length)
			),
			// This expands the relative paths to absolute paths, so e.g.
			// src/nested/foo becomes /project/src/nested/foo.js
			fileURLToPath(new URL(file, import.meta.url))
		])
	),
    output: [{ dir: "dist", format: "es" }],
    plugins: [dts.default()],
  },
];