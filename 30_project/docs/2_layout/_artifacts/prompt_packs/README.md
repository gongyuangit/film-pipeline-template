# Layout Prompt Packs

This folder contains the segment, shot, blender, and lookdev prompt packs that drive the respective branches. Each file must expose `globals.negative`, a `shots[]` array (or `segments[]`), and the `negative_effective = globals.negative + shots[].negative` convention described in the higher-level README.
