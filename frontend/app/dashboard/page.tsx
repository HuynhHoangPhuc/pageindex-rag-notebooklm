"use client";

import { useEffect, useState } from "react";
import { getDocuments } from "@/lib/api";
import { FileUploader } from "@/components/FileUploader";
import { ChatInterface } from "@/components/ChatInterface";
import { Button } from "@/components/ui/button";
// Checkbox removed
import { FileText, LogOut, Menu } from "lucide-react";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

// Basic checkbox
function SimpleCheckbox({ checked, onCheckedChange }: { checked: boolean; onCheckedChange: (c: boolean) => void }) {
    return (
        <input
            type="checkbox"
            checked={checked}
            onChange={(e) => onCheckedChange(e.target.checked)}
            className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />
    )
}

export default function DashboardPage() {
    const [documents, setDocuments] = useState<any[]>([]);
    const [selectedFileIds, setSelectedFileIds] = useState<string[]>([]);
    const [token, setToken] = useState("");

    const fetchDocs = async () => {
        const t = localStorage.getItem("token");
        if (!t) return; // redirect logic usually handled by layout/middleware
        setToken(t);
        try {
            const docs = await getDocuments(t);
            setDocuments(docs);
            // Auto select new docs? Maybe not.
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        fetchDocs();
    }, []);

    const toggleFile = (id: string, checked: boolean) => {
        if (checked) {
            setSelectedFileIds([...selectedFileIds, id]);
        } else {
            setSelectedFileIds(selectedFileIds.filter((fid) => fid !== id));
        }
    };

    const SidebarContent = () => (
        <div className="flex flex-col h-full gap-4">
            <div className="flex items-center gap-2 font-bold text-xl px-2">
                <span className="bg-blue-600 text-white p-1 rounded">PI</span> PageIndex RAG
            </div>

            <div className="p-2 bg-muted/50 rounded-lg">
                <FileUploader onUploadComplete={fetchDocs} />
            </div>

            <div className="flex-1 overflow-y-auto">
                <h3 className="text-sm font-semibold mb-2 px-2 text-muted-foreground">Sources</h3>
                {documents.length === 0 ? (
                    <p className="text-sm px-2 text-muted-foreground">No sources yet.</p>
                ) : (
                    <div className="space-y-1">
                        {documents.map((doc) => (
                            <div key={doc.id} className="flex items-center gap-2 p-2 hover:bg-muted/50 rounded cursor-pointer" onClick={() => toggleFile(doc.pageindex_file_id, !selectedFileIds.includes(doc.pageindex_file_id))}>
                                <SimpleCheckbox
                                    checked={selectedFileIds.includes(doc.pageindex_file_id)}
                                    onCheckedChange={(c) => toggleFile(doc.pageindex_file_id, c)}
                                />
                                <FileText className="w-4 h-4 text-blue-500" />
                                <span className="text-sm truncate max-w-[150px]" title={doc.filename}>{doc.filename}</span>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <div className="mt-auto pt-4 border-t">
                <Button variant="ghost" className="w-full justify-start text-red-500" onClick={() => {
                    localStorage.removeItem("token");
                    window.location.href = "/";
                }}>
                    <LogOut className="mr-2 h-4 w-4" /> Logout
                </Button>
            </div>
        </div>
    );

    return (
        <div className="flex h-screen bg-background text-foreground overflow-hidden">
            {/* Desktop Sidebar */}
            <aside className="hidden md:flex w-64 border-r p-4 flex-col bg-card">
                <SidebarContent />
            </aside>

            {/* Mobile Sidebar */}
            <div className="md:hidden">
                <Sheet>
                    <SheetTrigger asChild>
                        <Button variant="ghost" size="icon" className="absolute top-4 left-4 z-50">
                            <Menu />
                        </Button>
                    </SheetTrigger>
                    <SheetContent side="left">
                        <SidebarContent />
                    </SheetContent>
                </Sheet>
            </div>

            <main className="flex-1 flex flex-col relative w-full h-full">
                <header className="h-14 border-b flex items-center px-4 md:hidden">
                    <span className="ml-10 font-bold">PageIndex RAG</span>
                </header>
                <div className="flex-1 overflow-hidden">
                    <ChatInterface selectedFileIds={selectedFileIds} />
                </div>
            </main>
        </div>
    );
}
