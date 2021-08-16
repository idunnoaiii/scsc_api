<template>
  <v-layout>
    <v-row justify="center">
      <v-col cols="10">
        <v-data-table
          :headers="headers"
          :items="discounts"
          sort-by="created_date"
          class="elevation-1"
          width="90%"
          :search="search"
        >
          <template v-slot:[`item.type`]="{ item }">
            <span>{{ item.type == 0 ? "Percentage(%)" : "Cash" }}</span>
          </template>
          <template v-slot:[`item.is_apply`]="{ item }">
            <span>{{ item.is_apply == true ? "Yes" : "No" }}</span>
          </template>
        <template v-slot:[`item.value`]="{ item }">
            <span>{{ item.type == 0 ? item.value + '%' : item.value }}</span>
          </template>
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title class="text-h4"> Discounts</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-text-field
                v-model="search"
                label="Search"
                hide-details
                class="mx-4"
              ></v-text-field>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="500px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    v-bind="attrs"
                    v-on="on"
                  >
                    New
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-form ref="form" lazy-validation v-model="valid">
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.description"
                              label="Desciption"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.threshold"
                              label="Threshold*"
                              type="number"
                              step="1000"
                              min="0"
                              :rules="[required('Threshold'), greaterThan(0)]"
                            ></v-text-field>
                          </v-col>

                          <v-col cols="12" md="12">
                            <v-select
                              :items="types"
                              v-model="editedItem.type"
                              label="Type discount"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.value"
                              label="Value*"
                              type="number"
                              min="0"
                              :step="editedItem.type == 1 ? 1000 : 0.1"
                              :rules="[required('value'), greaterThan(0)]"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" md="12">
                            <v-switch
                              v-model="editedItem.is_apply"
                              :label="`Is Apply : ${
                                editedItem.is_apply == true ? 'Yes' : 'No'
                              }`"
                            ></v-switch>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-form>
                    <small>*indicates required field</small>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="blue darken-1"
                      class="white--text"
                      @click="close"
                      text
                    >
                      Cancel
                    </v-btn>
                    <v-btn
                      color="green darken-1"
                      class="white--text"
                      @click="save"
                      :disabled="!valid"
                    >
                      Save
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5"
                    >Are you sure you want to delete this item?</v-card-title
                  >
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="blue darken-1"
                      class="white--text"
                      @click="closeDelete"
                      text
                      >Cancel</v-btn
                    >
                    <v-btn
                      color="red darken-1"
                      class="white--text"
                      @click="deleteItemConfirm"
                      >OK</v-btn
                    >
                    <v-spacer></v-spacer>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
          </template>
          <template v-slot:no-data>
            <v-btn color="primary" @click="load"> Reset </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-layout>
</template>
<script>
import axios from "../../axios";
export default {
  data: () => ({
    valid: true,
    dialog: false,
    password: "",
    search: "",
    dialogDelete: false,
    headers: [
      {
        text: "Description",
        align: "start",
        value: "description",
      },
      { text: "Threshold", value: "threshold" },
      { text: "Type", value: "type", sortable: false },
      { text: "Value", value: "value", sortable: false },
      { text: "Apply", value: "is_apply", sortable: false },
      { text: "Action", value: "actions", sortable: false },
    ],
    discounts: [],
    editedIndex: -1,
    editedItem: {
      description: "",
      threshold: 0,
      type: 0,
      value: 0,
      is_apply: false,
    },
    defaultItem: {
      description: "",
      threshold: 0,
      type: 0,
      value: 0,
      is_apply: false,
    },
    types: [
      {
        text: "Percentage(%)",
        value: 0,
      },
      {
        text: "Cash",
        value: 1,
      },
    ],
    roleSelected: false,
    required(inputName) {
      return (v) => (v && v.toString().length > 0) || `${inputName} is required.`;
    },
    // noSpace() {
    //   return (v) => (v || "").indexOf(" ") < 0 || "No spaces are allowed";
    // },
    greaterThan(value){
      return (v) => (v && Number(v) >= value) || `Must greater than ${value}!`
    }
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Discount" : "Edit Discount";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  // created() {
  //   this.initialize();
  // },

  mounted() {
    this.load();
  },
  methods: {
    load() {
      axios
        .get("api/v1/discounts/?skip=0&limit=100")
        .then((response) => {
          this.discounts = response.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    editItem(item) {
      this.editedIndex = this.discounts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.password = "";
    },

    deleteItem(item) {
      this.editedIndex = this.discounts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      // this.users.splice(this.editedIndex, 1);
      axios
        .delete(`/api/v1/users/${this.editedItem.id}`)
        .then((response) => {
          if (response.status == 200) {
             this.$store.commit("SET_TOAST", {
              toastMsg: "Discount deleted!",
              toastColor: "green",
            });
            this.load();
          }
        })
        .catch((err) => {
          console.log(err);
        });

      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$refs.form.reset();
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (!this.$refs.form.validate()) {
        return;
      }

      const item = {
        description: this.editedItem.description,
        threshold: this.editedItem.threshold,
        type: this.editedItem.type,
        value: this.editedItem.value,
        is_apply: this.editedItem.is_apply,
      };

      if (this.editedIndex > -1) {
        //update

        item.id = this.editedItem.id;
        axios
          .put("/api/v1/discounts/", item)
          .then(() => {
            this.load();
             this.$store.commit("SET_TOAST", {
              toastMsg: "Discount updated!",
              toastColor: "green",
            });
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        //add
        axios
          .post("/api/v1/discounts/", item)
          .then(() => {
            this.load();
             this.$store.commit("SET_TOAST", {
              toastMsg: "Discount added!",
              toastColor: "green",
            });
          })
          .catch((err) => {
            console.log(err);
          });
      }
      this.close();
    },

    filterUser(value, search, items) {
      console.log(items);
      return (
        value != null &&
        search != null &&
        typeof value === "string" &&
        value.toString().indexOf(search) !== -1
      );
    },
  },
};
</script>