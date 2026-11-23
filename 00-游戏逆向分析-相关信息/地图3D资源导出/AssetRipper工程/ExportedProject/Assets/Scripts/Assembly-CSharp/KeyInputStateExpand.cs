using UnityEngine;

public static class KeyInputStateExpand
{
	public static bool IsTouched(this KeyInputState state)
	{
		return false;
	}

	public static KeyInputState GetKeyState(KeyCode keyCode)
	{
		return KeyInputState.Unpressed;
	}
}
