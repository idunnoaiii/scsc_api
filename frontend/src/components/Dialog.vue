<template>
  <v-row justify="center">
    <v-dialog
      v-model="$store.state.dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="deep-purple">
          <v-btn icon dark @click="$store.commit('SHOW_GLOBAL_DIALOG')">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title><slot name="dialogName"></slot></v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn dark text @click="dialog = false"> Save </v-btn>
          </v-toolbar-items>
        </v-toolbar>

        <v-divider></v-divider>
        <slot name=dialogBody>This is dialog body</slot>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {

};
</script>