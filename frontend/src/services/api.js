import axios from "axios";

const api = axios.create({
    baseURL:
        import.meta.env.VITE_API_URL ||
        "http://127.0.0.1:8000",

    headers: {
        "Content-Type": "application/json",
    },
});

export const sendMessage = async (message, sessionId) => {

    const response = await api.post("/chat", {
        message: message,
        session_id: sessionId
    });

    return response.data;
};

export const getConversations = async () => {
    const response = await api.get("/conversations/");
    return response.data;
};


export const getConversation = async (sessionId) => {
    const response = await api.get(
        `/conversations/${sessionId}`
    );

    return response.data;
};


export const deleteConversation = async (sessionId) => {
    const response = await api.delete(
        `/conversations/${sessionId}`
    );

    return response.data;
};

export default api;