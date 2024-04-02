import { MessageContextProvider } from "./MessageContextProvider";
import { ResponseContextProvider } from "./ResponseContextProvider";
import { AppProvider } from "./ShowSettingsHandler";
import { DarkModeContextProvider } from "./DarkModeContextProvider";
import { ShowInfoWindowContextProvider } from "./ShowInfoWindowContextProvider";
import { AuthContextProvider } from "./AuthContextProvider";

function ContextProvider({ children }) {
  return (
    <AuthContextProvider>
      <ShowInfoWindowContextProvider>
        <DarkModeContextProvider>
          <ResponseContextProvider>
            <MessageContextProvider>
              <AppProvider>{children}</AppProvider>
            </MessageContextProvider>
          </ResponseContextProvider>
        </DarkModeContextProvider>
      </ShowInfoWindowContextProvider>
    </AuthContextProvider>
  );
}

export default ContextProvider;
