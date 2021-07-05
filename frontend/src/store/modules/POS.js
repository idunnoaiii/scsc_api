import axios from '../../axios'

const state = () => ({
	orderItems: [],
	customer_checkout: 0,
	totalItem: 0,
	totalPrice: 0,
	// paymentAmount: 0,
	// tax: 10,
	checkoutStatus: null,
	showBillDialog: false,
})

const getters = {
	totalOrderItem(state) {
		return state.orderItems.reduce((acc, item) => acc + item.quantity, 0)
	},
	totalPrice(state) {
		return state.orderItems.reduce((acc, item) => acc + (item.quantity * item.price), 0)
	}
}

const actions = {
	checkout({ commit, state, getters }, payload) {

		let orderDetail = {
			code: new Date().getTime(),
			user_id: 1,
			status: true,
			tax: 0,
			subtotal: getters.totalPrice,
			paid: payload.amount,
			change: payload.change,
			order_items: [
				{
					item_id: 0,
					price: 0,
					quantity: 0,
					item_name: "string",
				},
			],
		};

		orderDetail.order_items = state.orderItems.map((item) => ({
			item_id: item.id,
			price: item.price,
			quantity: item.quantity,
			item_name: item.name,
		}));

		axios
			.post("/api/v1/orders/", orderDetail)
			.then(() => {
				commit('SET_CHECKOUT_STATUS', true)
				commit('CLEAR_ORDER_ITEM')
			})
			.catch((err) => {
				console.log(err);
				commit('SET_CHECKOUT_STATUS', false)
			});

	},
}

const mutations = {
	ADD_ITEM_TO_ORDER(state, item) {
		let itemIndex = state.orderItems.findIndex(x => x.id == item.id);
		if (itemIndex > -1) {
			state.orderItems[itemIndex].quantity++;
			return
		}
		let orderItem = {
			id: item.id,
			rownumber: state.orderItems.length + 1,
			name: item.name,
			quantity: 1,
			price: item.price,
		};
		state.orderItems.push(orderItem)
	},

	SET_CHECKOUT_STATUS(state, status) {
		state.checkoutStatus = status;
	},

	INCREASE_ITEM_QUANTITY(state, id) {
		let item = state.orderItems.find(x => x.id == id)
		if (item) item.quantity++
	},

	DECREASE_ITEM_QUANTITY(state, id) {
		let item = state.orderItems.find(x => x.id == id)
		if(item == null || item == undefined) 
			return;
		if (item.quantity > 1) {
			item.quantity--;
			return;
		}
		state.orderItems = state.orderItems.filter(x => x.id != id);
	},

	CLEAR_ORDER_ITEM(state){
		state.orderItems = [];
	},

	SET_BILL_DIALOG(state, status){
		state.showBillDialog = status;
	},


	CLEAR_CHECKOUT_DATA(state){
		state.orderItems = [];
	}

}


export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations
}