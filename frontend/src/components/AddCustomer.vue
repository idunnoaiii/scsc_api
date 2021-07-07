<template>
  <v-form ref="form" lazy-validation v-model="valid">
    <v-container>
      <v-row>
        <v-col cols="12" sm="6" md="12">
          <v-text-field
            label="Phone*"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6" md="12">
          <v-text-field
            label="Name"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
export default {
    
}
</script>