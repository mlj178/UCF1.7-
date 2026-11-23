using UnityEngine;
using UnityEngine.UI;

public class HUD_ScreenFX : Singleton<HUD_ScreenFX>
{
	[SerializeField]
	private RawImage nanoScreenImage;

	private NameKeyPool pool;

	protected override void Awake()
	{
	}

	private void Update()
	{
	}

	public static RecyclableObject AddEffect(GameObject pfb, bool autoActive)
	{
		return null;
	}
}
