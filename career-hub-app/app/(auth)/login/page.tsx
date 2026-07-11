"use client"

import { Card, TextInput, Title } from "@mantine/core";

export default function LoginPage() {

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);

        const {email, password} = Object.fromEntries(formData);
        console.log(email, password);
    }


    return (
        <div>
            <Card shadow="sm" padding="lg" radius="md" withBorder>
                <Title order={2} size="xl">Login</Title>
                <form onSubmit={handleSubmit}>
                    <TextInput name="email" label="Email" placeholder="Enter your email" required />
                    <TextInput name="password" label="Password" placeholder="Enter your password" type="password" required />
                    <button type="submit">Login</button>
                </form>
            </Card>
        </div>
    )

}