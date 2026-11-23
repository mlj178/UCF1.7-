using UnityEngine;
using UnityEngine.UI;

public class HUD_Nano6_BuffIcon : RecyclableObject
{
	[SerializeField]
	private Image image;

	private Vector3 targetPos;

	private bool isRadar;

	public void SetSprite(Sprite sprite, bool isRadar)
	{
	}

	public void SetBornPosAndTartgetPos(Vector3 born, Vector3 target)
	{
	}

	protected override void Work()
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}
}
