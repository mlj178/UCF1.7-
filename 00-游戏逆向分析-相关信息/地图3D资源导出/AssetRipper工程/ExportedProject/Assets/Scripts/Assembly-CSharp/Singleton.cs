using UnityEngine;

public class Singleton<T> : MonoBehaviour where T : Singleton<T>
{
	protected static GameObject inspector;

	public static T instance { get; private set; }

	public static bool visible => false;

	public static bool isInitialized => false;

	protected virtual void Awake()
	{
	}

	protected virtual void OnDestroy()
	{
	}

	public virtual void SetVisible(bool visible)
	{
	}
}
