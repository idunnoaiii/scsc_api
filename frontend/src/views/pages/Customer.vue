<template>
  <v-layout>
    <v-row justify="center">
      <v-col cols="10">
        <v-data-table
          :headers="headers"
          :items="customers"
          sort-by="calories"
          class="elevation-1"
          width="90%"
          :search="search"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title class="text-h4"> Customer</v-toolbar-title>
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
                              v-model="editedItem.contact"
                              label="Contact*"
                              :rules="[required('Username'), isPhone()]"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.name"
                              label="Name"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.address"
                              label="Address"
                            ></v-text-field>
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
                    >Are you sure you want to delete this user?</v-card-title
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
    search: "",
    dialogDelete: false,
    headers: [
      { text: "Contact", value: "contact" },
      {
        text: "Customer Name",
        align: "start",
        value: "name",
      },
      { text: "address", value: "address" },
      { text: "Action", value: "actions", sortable: false },
    ],
    customers: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      contact: "",
      address: "",
    },
    defaultItem: {
      name: "",
      contact: "",
      address: "",
    },
    roleSelected: false,
    required(inputName) {
      return (v) => (v && v.length > 0) || `${inputName} is required.`;
    },
    noSpace() {
      return (v) => (v || "").indexOf(" ") < 0 || "No spaces are allowed";
    },
    isPhone() {
      let re = /(0[3|5|7|8|9])+([0-9]{8})\b/;
      return (v) => (v && re.test(v)) || `Not a valid phone number.`;
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Customer" : "Edit Customer";
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
        .get("api/v1/customers")
        .then((response) => {
          this.customers = response.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    editItem(item) {
      this.editedIndex = this.customers.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.customers.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      // this.customers.splice(this.editedIndex, 1);
      axios
        .delete(`api/v1/customers/${this.editedItem.id}`)
        .then((response) => {
          if (response.status == 200) {
             this.$store.commit("SET_TOAST", {
              toastMsg: "Customer deleted!",
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

      const customerObj = {
        contact: this.editedItem.contact,
        name: this.editedItem.name,
        address: this.editedItem.address
      };

      if (this.editedIndex > -1) {
        //update
        customerObj.id = this.editedItem.id;
        axios
          .put("/api/v1/customers/", customerObj)
          .then(() => {
            this.load();
             this.$store.commit("SET_TOAST", {
              toastMsg: "Customer updated!",
              toastColor: "green",
            });
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        //add


        axios
          .post("/api/v1/customers/", customerObj)
          .then(() => {
            this.load();
             this.$store.commit("SET_TOAST", {
              toastMsg: "Customer added!",
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