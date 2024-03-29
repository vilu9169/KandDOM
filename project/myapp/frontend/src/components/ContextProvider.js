import { MessageContextProvider } from "./MessageContextProvider";
import { ResponseContextProvider } from "./ResponseContextProvider";
import { AppProvider } from "./ShowSettingsHandler";
import { DarkModeContextProvider } from "./DarkModeContextProvider";


function ContextProvider({ children }) {

  return (
    <DarkModeContextProvider>
    <ResponseContextProvider>
    <MessageContextProvider>
    <AppProvider>
      {children}
      </AppProvider>
    </MessageContextProvider>
    </ResponseContextProvider>
    </DarkModeContextProvider>
  );
}

export default ContextProvider;