import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [output, setOutput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [stdin, setInput] = useState("");
  
  
  const handleSubmit = async () => {
    setIsLoading(true);
    setOutput(""); // Clear previous output
  
    try {
      const response = await axios.post("http://localhost:8000/submit", {
        code,
        language,
        stdin,
      });
  
      // Check if the backend response contains 'output'
      if (response.data && response.data.output) {
        setOutput(response.data.output); // Set the output from response
      } else {
        setOutput("No output returned."); // Handle the case where no output is returned
      }
  
      console.log(response.data.output); // Log output to console for debugging
    } catch (error) {
      setOutput("An error occurred.");
      console.error(error); // Log the error for debugging
    } finally {
      setIsLoading(false); // Set loading to false after request is done
    }
  };
  
  // const handleSubmit = async () => 
  //   {
  //   setIsLoading(true);
  //   setOutput("");
  

  //   try {
  //     const response = await axios.post("http://localhost:8000/submit", {
  //       code,
  //       language,
  //     })
  //     // .then(response => response.json())
  //     // .then(data => {document.getElementById("output").innerText = data.output || data.error;})
  //     console.log(response.data.output)
  //     setOutput(response.data.output || "No output returned.");
  //   } catch (error) {
  //     setOutput("An error occurred.");
  //   } finally {
  //     setIsLoading(false);
  //   }
  // };

  return (
    <><div className="top-pane">

      <h1>CODING JUDGE</h1>
      
    </div>
    <div className="container">
        {/* Output Section */}
        <div className="left-pane">
          <h2>Output</h2>
          <pre id="output">{output}</pre>
        </div>

        {/* Code Input Section */}
        <div className="right-pane">
          <div className="select-pane">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="python">Python</option>
              <option value="cpp">C++</option>
              <option value="java">Java</option>
              <option value="c">C</option>
            </select>
            
          </div>
          
          <textarea className="coding"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Write your code here..." />
          <textarea className="stdin"
            value={stdin}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Provide standard input here..."
          />
          <div className="bottom-pane">
            <button onClick={handleSubmit} disabled={isLoading}>
              {isLoading ? "Submitting..." : "Submit"}
            </button>
          </div>  
        </div>
      </div>
      
    </>
  );
}

export default App;

// function App() {
//   const [code, setCode] = useState("");
//   const [language, setLanguage] = useState("python");
//   const [input, setInput] = useState(""); // New state for stdin
//   const [output, setOutput] = useState("");
//   const [isLoading, setIsLoading] = useState(false);

//   const handleSubmit = async () => {
//     setIsLoading(true);
//     setOutput("");

//     try {
//       const response = await axios.post("http://localhost:8000/submit", {
//         code,
//         language,
//         stdin: input, // Pass stdin to the backend
//       });

//       setOutput(response.data.output || "No output returned.");
//     } catch (error) {
//       setOutput("An error occurred.");
//       console.error(error);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="container">
//       <div className="top-pane">
//         <h1>CODING JUDGE</h1>
//       </div>
//       <div className="main-pane">
//         <div className="left-pane">
//           <h2>Output</h2>
//           <pre id="output">{output}</pre>
//         </div>
//         <div className="right-pane">
//           <div className="select-pane">
//             <select
//               value={language}
//               onChange={(e) => setLanguage(e.target.value)}
//             >
//               <option value="python">Python</option>
//               <option value="cpp">C++</option>
//               <option value="java">Java</option>
//               <option value="c">C</option>
//             </select>
//           </div>
//           <textarea
//             value={code}
//             onChange={(e) => setCode(e.target.value)}
//             placeholder="Write your code here..."
//           />
//           <textarea
//             value={input}
//             onChange={(e) => setInput(e.target.value)}
//             placeholder="Provide standard input here..."
//           />
//           <div className="bottom-pane">
//             <button onClick={handleSubmit} disabled={isLoading}>
//               {isLoading ? "Submitting..." : "Submit"}
//             </button>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;
