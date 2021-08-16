<template>
  <v-dialog v-model="showDialog" max-width="500px">
    <v-card>
      <v-card-title class="text-h5"
        >
        <slot name="title"></slot>
        </v-card-title
      >
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="$emit('close-delete')"
          >Cancel</v-btn
        >
        <v-btn color="blue darken-1"  @click="$emit('delete-item-confirm')"
          >OK</v-btn
        >
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "DialogDeleteItem",
  props:["showDialog"],
  data: function () {
    return {
    };
  },
  methods: {
  },
};
</script>