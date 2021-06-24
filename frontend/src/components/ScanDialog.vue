<template>
  <v-row justify="center">
    <v-dialog
      v-model="$store.state.scanDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="$store.commit('TOGGLE_SCAN_DIALOG')">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title><slot name="dialogName"></slot></v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn dark text @click="$store.commit('TOGGLE_SCAN_DIALOG')">
              Save
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>

        <v-divider></v-divider>
        <v-card class="d-flex pa-2" outlined tile>
          <div>I'm an inline flexbox container!</div>
        </v-card>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {};
</script>