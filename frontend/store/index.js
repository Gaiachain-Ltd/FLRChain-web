const DETAILS_PROJECT_ID = "details_project_id";

export const state = () => ({
    regEmail: '',
    drawerState: null,
    detailsProjectId: parseInt(localStorage.getItem(DETAILS_PROJECT_ID))
})

export const getters = {
    isAuthenticated(state) {
        return state.auth.loggedIn
    },

    loggedInUser(state) {
        return state.auth.user
    },

    isFacililator(state) {
        return state.auth.user.type === 1;
    },

    isInvestor(state) {
        return state.auth.user.type === 2;
    },

    regEmail(state) {
        return state.regEmail;
    },
    getDrawerState(state) {
        return state.drawerState
    },
    getDetailsProjectId(state) {
        return state.detailsProjectId;
    }
}

export const mutations = {
    setRegEmail(state, email) {
        state.regEmail = email;
    },
    setDrawerState(state, value) {
        state.drawerState = value;
    },
    setDetailsProjectId(state, value) {
        state.detailsProjectId = value;
        localStorage.setItem(DETAILS_PROJECT_ID, value);
    }
}

export const actions = {
    updateRegEmail({ commit }, email) {
        commit('setRegEmail', email);
    },
    updateDrawerState({ commit }, value) {
        commit('setDrawerState', value);
    },
    updateDetailsProjectId({ commit }, value) {
        commit("setDetailsProjectId", value);
    }
}
