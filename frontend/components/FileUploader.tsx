"use client";

import { useState } from "react";
import { uploadFile } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, Upload } from "lucide-react";

export function FileUploader({ onUploadComplete }: { onUploadComplete: () => void }) {
    const [uploading, setUploading] = useState(false);

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setUploading(true);
            try {
                const token = localStorage.getItem("token") || "";
                await uploadFile(e.target.files[0], token);
                onUploadComplete();
            } catch (error) {
                console.error(error);
                alert("Upload failed");
            } finally {
                setUploading(false);
            }
        }
    };

    return (
        <div className="flex items-center gap-2">
            <Input
                type="file"
                id="file-upload"
                className="hidden"
                onChange={handleFileChange}
            />
            <Button disabled={uploading} asChild variant="outline" className="w-full justify-start cursor-pointer">
                <label htmlFor="file-upload">
                    {uploading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Upload className="mr-2 h-4 w-4" />}
                    {uploading ? "Uploading..." : "Add Source"}
                </label>
            </Button>
        </div>
    );
}
