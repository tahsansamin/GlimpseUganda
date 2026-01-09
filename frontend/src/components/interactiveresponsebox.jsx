import React from "react";

export default function Box({ mmessages = [] }) {
    return (
        <div className="w-full max-w-4xl mx-auto p-4 space-y-3">
            {mmessages.map((message, index) => {
                if (message.typeofMessage === "user"){
                    return (
                        <div key={index} className="flex justify-end">
                            <div className="max-w-[80%] sm:max-w-[70%] bg-blue-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 shadow-sm">
                                <p className="text-sm sm:text-base leading-relaxed">{message.text}</p>
                            </div>
                        </div>
                    )
                }
                if (message.typeofMessage === "chatresponse"){
                    return (
                        <div key={index} className="flex justify-start">
                            <div className="max-w-[80%] sm:max-w-[70%] bg-gray-100 text-gray-900 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
                                <p className="text-sm sm:text-base leading-relaxed">{message.text}</p>
                            </div>
                        </div>
                    )
                }
                return null;
            })}
        </div>
    )
}
