import { MessageContextProvider } from "./MessageContextProvider";
import { ResponseContextProvider } from "./ResponseContextProvider";
import { AppProvider } from "./ShowSettingsHandler";
import { DarkModeContextProvider } from "./DarkModeContextProvider";
import { ShowInfoWindowContextProvider } from "./ShowInfoWindowContextProvider";

function ContextProvider({ children }) {

  return (
    <ShowInfoWindowContextProvider>
    <DarkModeContextProvider>
    <ResponseContextProvider>
    <MessageContextProvider>
    <AppProvider>
      {children}
      </AppProvider>
    </MessageContextProvider>
    </ResponseContextProvider>
    </DarkModeContextProvider>
    </ShowInfoWindowContextProvider>
  );
}

export default ContextProvider;