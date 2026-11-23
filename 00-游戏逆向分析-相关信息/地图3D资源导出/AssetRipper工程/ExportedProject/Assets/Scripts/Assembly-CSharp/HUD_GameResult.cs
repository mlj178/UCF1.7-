using UnityEngine;
using UnityEngine.UI;

public class HUD_GameResult : Singleton<HUD_GameResult>
{
	private Image image;

	[SerializeField]
	private Sprite[] sprites;

	protected override void Awake()
	{
	}

	public static void Show(int index)
	{
	}

	private void Hide()
	{
	}
}
