<template>
  <v-row justify="center">
    <v-dialog
      v-model="$store.state.dialog"
      max-width="620px"
      hide-overlay
      transition="dialog-bottom-transition"
    >
    <v-card>
      <v-card-title class="text-h5"
        >
        <slot name="title"></slot>
        </v-card-title
      >
      <v-card-text>
        <slot name="dialogBody"></slot>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="$emit('close-delete')"
          >Cancel</v-btn
        >
        <v-btn color="blue darken-1" text @click="$emit('delete-item-confirm')"
          >OK</v-btn
        >
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {};
</script>