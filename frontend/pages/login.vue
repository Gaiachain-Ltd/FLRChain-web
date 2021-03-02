<template>
    <v-container fluid fill-height>
        <v-layout column align-center justify-center>
            <AuthCard title="Login" subtitle="Welcome back!"></AuthCard>
        </v-layout>
    </v-container>
</template>

<script>
export default {
    components: {
        AuthCard: () => import("@/components/cards/AuthCard")
    }
}
</script>