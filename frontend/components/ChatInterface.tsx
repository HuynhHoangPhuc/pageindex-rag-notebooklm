"use client";

import { useState, useRef, useEffect } from "react";
import { chat } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { Send, Bot, User as UserIcon, Loader2 } from "lucide-react";

interface Message {
    role: "user" | "bot";
    content: string;
}

export function ChatInterface({ selectedFileIds }: { selectedFileIds: string[] }) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages, loading]);

    const handleSend = async () => {
        if (!input.trim() || selectedFileIds.length === 0) return;

        if (selectedFileIds.length === 0) {
            alert("Please select at least one source to chat with.");
            return;
        }

        const userMsg: Message = { role: "user", content: input };
        setMessages((prev) => [...prev, userMsg]);
        setInput("");
        setLoading(true);

        try {
            const token = localStorage.getItem("token") || "";
            const res = await chat(userMsg.content, selectedFileIds, token);

            // Handle response structure.
            // If backend returns string directly or object
            // Backend: return response (which might be object or string)
            // app/mcp_server returns string. app/api returns object.
            // Let's assume object similar to OpenAI or just text content.
            let content = "";
            if (typeof res === 'string') content = res;
            else if (res.choices && res.choices[0]) content = res.choices[0].message.content;
            else if (res.message) content = res.message; // Fallback
            else content = JSON.stringify(res);

            const botMsg: Message = { role: "bot", content };
            setMessages((prev) => [...prev, botMsg]);
        } catch (err) {
            setMessages((prev) => [...prev, { role: "bot", content: "Error getting response." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full">
            <ScrollArea className="flex-1 p-4">
                <div className="space-y-4">
                    {messages.length === 0 && (
                        <div className="text-center text-gray-500 mt-10">
                            <h3 className="text-lg font-semibold">Welcome to PageIndex RAG</h3>
                            <p>Select a source on the left and start chatting.</p>
                        </div>
                    )}
                    {messages.map((m, i) => (
                        <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                            <div className={`flex items-start gap-2 max-w-[80%] ${m.role === "user" ? "flex-row-reverse" : ""}`}>
                                <div className={`p-2 rounded-full ${m.role === "user" ? "bg-blue-500" : "bg-gray-200 dark:bg-gray-700"}`}>
                                    {m.role === "user" ? <UserIcon className="w-4 h-4 text-white" /> : <Bot className="w-4 h-4" />}
                                </div>
                                <Card className={`p-3 ${m.role === "user" ? "bg-blue-500 text-white" : "bg-gray-100 dark:bg-gray-800"}`}>
                                    <p className="whitespace-pre-wrap text-sm">{m.content}</p>
                                </Card>
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="flex justify-start">
                            <div className="flex items-center gap-2 bg-gray-100 dark:bg-gray-800 p-3 rounded-lg">
                                <Loader2 className="w-4 h-4 animate-spin" />
                                <span className="text-sm">Thinking...</span>
                            </div>
                        </div>
                    )}
                    <div ref={scrollRef} />
                </div>
            </ScrollArea>
            <div className="p-4 border-t bg-background">
                <div className="flex gap-2">
                    <Input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask something about your sources..."
                        onKeyDown={(e) => e.key === "Enter" && handleSend()}
                    />
                    <Button onClick={handleSend} disabled={loading || selectedFileIds.length === 0}>
                        <Send className="w-4 h-4" />
                    </Button>
                </div>
            </div>
        </div>
    );
}
